import requests
from jinja2 import TemplateNotFound

from app import app
from flask import render_template, make_response, request, json
from .libs.db import *
from .libs.SFTP import *

from concurrent.futures import ThreadPoolExecutor
from threading import Thread

executor = ThreadPoolExecutor(TASK_THREAD_POOL_SIZE)

db_monitor = DbMonitor()
# 初始化日志文件
if not os.path.exists('logs'):
    os.makedirs('logs')
if not os.path.exists(DATA_SAVE_DIR):
    os.makedirs(DATA_SAVE_DIR)

init_log(logging.DEBUG, logging.DEBUG, logfile=os.path.join('logs', str(os.path.split(__file__)[1].split(".")[0]) + '_debug.log'))
init_log(logging.ERROR, logging.ERROR, logfile=os.path.join('logs', str(os.path.split(__file__)[1].split(".")[0]) + '.log'))


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('natural_semantic.html')


@app.route('/natural_semantic', methods=['GET', 'POST'])
def natural_semantic():
    return render_template('natural_semantic.html')


@app.route('/image_identification', methods=['GET', 'POST'])
def image_identification():
    return render_template('image_identification.html')


@app.route('/index')
def index1():
    return render_template('index.html')


@app.route('/index2')
def index2():
    return render_template('index2.html')


@app.route('/query_data', methods=['POST'])
def query_data():
    r = request
    result = request.form.to_dict()
    page_size = result['page_size']
    page_number = result['page_num']
    if not page_size:
        page_size = 10
    if not page_number:
        page_number = 1
    # 查询数据库中的数据返回
    result = db_monitor.list_data(int(page_size), int(page_number))
    data = dict()
    data['rows'] = result
    data['total'] = db_monitor.count()
    return json.dumps(data)


def request_read_text_check(search_string):
    url = TEXT_CHECK_URL % search_string
    result = requests.get(url=url)
    return result.content


@app.route('/text_check', methods=['POST'])
def text_check():
    request_data = request.form.to_dict()
    search_string = request_data['search_string']
    return request_read_text_check(search_string)


@app.route('/pages/<item>')
def pages(item):
    return to_template(item)


@app.route('/pages/charts/<item>')
def pages_charts(item):
    return to_template(item)


@app.route('/pages/forms/<item>')
def pages_forms(item):
    return to_template(item)


@app.route('/pages/layout/<item>')
def pages_layout(item):
    return to_template(item)


@app.route('/pages/mailbox/<item>')
def pages_mailbox(item):
    return to_template(item)


@app.route('/pages/tables/<item>')
def pages_tables(item):
    return to_template(item)


@app.route('/pages/UI/<item>')
def pages_UI(item):
    return to_template(item)


@app.route('/pages/examples/<item>')
def pages_examples(item):
    return to_template(item)


@app.route('/upload_images', methods=['GET', 'POST'])
def upload_images():
    if request.files.getlist('file_data'):
        # 网上说此种方法可以，测试不行
        # executor.submit(handle_images(request.files.getlist('file_data')))
        images = request.files.getlist('file_data')
        save_images = list()
        save_image_paths = list()
        for image in images:
            file_name = get_random_str(3) + str(image.filename)
            file_path = os.path.join(DATA_SAVE_DIR, file_name)
            image.save(file_path)
            db_monitor.save_image(image_info={'path': file_path})
            save_images.append(file_name)
            save_image_paths.append(file_path)
        handle_image_async(save_images, save_image_paths)
        return json.dumps('{"state":"success"}'), 200


def to_template(item):
    path = request.path.strip('/')
    template = path
    if 'html' not in item:
        template = template + '.html'
    return render_template(template)


@app.errorhandler(404)
def page_not_found(error):
    # 找不到的页面定向到404
    resp = make_response(render_template('pages/examples/404.html'), 404)
    resp.headers['X-Something'] = 'A value'
    return resp


@app.errorhandler(TemplateNotFound)
def page_not_found(error):
    # 资源找不到也定向到404页面
    resp = make_response(render_template('pages/examples/404.html'), 404)
    resp.headers['X-Something'] = 'A value'
    return resp


def handle_images(images):
    """
    后台处理任务
    :param images:
    :return:
    """
    time.sleep(5)
    for image in images:
        file_name = get_random_str(3) + str(image.filename)
        file_path = os.path.join(DATA_SAVE_DIR, file_name)
        image.save(file_path)
        db_monitor.save_image(image_info={'path': file_path})


def async(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()

    return wrapper


def transfer_file(image_paths):
    """
    传递文件
    :param image_paths:
    :return:
    """
    try:
        remote_dir = REMOTE_SFTP_PATH
        local_paths = image_paths
        sftp_monitor = SFTP(host=SFTP_HOST_10, port=SFTP_PORT_10, user=SFTP_USER_10, pwd=SFTP_PWD_10)
        sftp_monitor.upload_file(remote_dir=remote_dir, local_paths=local_paths)
        sftp_monitor = SFTP(host=SFTP_HOST_11, port=SFTP_PORT_11, user=SFTP_USER_11, pwd=SFTP_PWD_11)
        sftp_monitor.upload_file(remote_dir=remote_dir, local_paths=local_paths)
        return True
    except Exception as e:
        error('SFTP文件传送失败：%s' % str(image_paths))
        error(str(e))
        return False


def get_politics_result(remote_path, local_path):
    """
    获取涉政结果
    """
    try:
        debug('获取涉政结果请求：%s' % remote_path)
        start = time.time()
        url = POLITICS_URL % remote_path.replace('/', '%2F')
        result = requests.get(url=url, timeout=20)
        if result.status_code == 200:
            debug('涉政：%s，%s' % (remote_path, result.content))
            result = json.loads(result.content)
            politics = result['result']
            cost = round((time.time() - start), 2)
            db_monitor.update_image_politics(local_path, cost, politics)

    except Exception as e:
        error(str(e), get_current_func_name())


def get_porn_result_new(remote_path, local_path):
    """
    获取鉴黄结果
    """
    try:
        debug('获取鉴黄结果请求：%s' % remote_path)
        start = time.time()
        url = PORN_URL % remote_path.replace('/', '%2F')
        result = requests.get(url=url, timeout=20)
        if result.status_code == 200:
            debug('鉴黄：%s，%s' % (remote_path, result.content))
            result = json.loads(result.content)
            porn = result['porn_level']
            cost = round((time.time() - start), 2)
            db_monitor.update_image_porn_new(local_path, cost, porn)

    except Exception as e:
        error(str(e), get_current_func_name())


def get_porn_result(remote_path, local_path):
    """
    获取鉴黄结果
    """
    try:
        debug('获取鉴黄结果请求：%s' % remote_path)
        data = {'data': remote_path}
        start = time.time()
        result = requests.post(url=PORN_URL, data=data, timeout=20)
        if result.status_code == 200:
            result = json.loads(result.content)
            porn, sexy, normal = 0, 0, 0
            for item in result['prediction'][0]:
                probability = item['probability']
                if item['class'] == 'porn':
                    porn = probability
                if item['class'] == 'sexy':
                    sexy = probability
                if item['class'] == 'normal':
                    normal = probability
            cost = round((time.time() - start), 2)
            db_monitor.update_image_porn(local_path, cost, porn, sexy, normal)

    except Exception as e:
        error(str(e), get_current_func_name())


@async
def handle_image_async(image_names, image_paths):
    """
    后台处理任务（请求接口）
    """
    # 传送文件
    if transfer_file(image_paths):
        # 传送成功才发送请求
        for image_path in image_names:
            remote_path = os.path.join(REMOTE_SFTP_PATH, image_path)
            local_path = os.path.join(DATA_SAVE_DIR, image_path)
            get_porn_result_new(remote_path, local_path)
            get_politics_result(remote_path, local_path)


def write_file_log(msg, module='', level='error'):
    filename = os.path.split(__file__)[1]
    if level == 'debug':
        logging.getLogger().debug('File:' + filename + ', ' + module + ': ' + msg)
    elif level == 'warning':
        logging.getLogger().warning('File:' + filename + ', ' + module + ': ' + msg)
    else:
        logging.getLogger().error('File:' + filename + ', ' + module + ': ' + msg)


# 调试日志
def debug(msg, func_name=''):
    module = "%s" % func_name
    write_file_log(msg, module, 'debug')


# 错误日志
def error(msg, func_time=''):
    module = "%s" % func_time
    write_file_log(msg, module, 'error')
