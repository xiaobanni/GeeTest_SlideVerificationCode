from PIL import Image #获取图像R阿GB值
def get_gap_left(image2):
    """
    获取滑块左端位置及滑块大小
    :param image2: 带缺口的图片
    :return: 滑块左端位置，滑块大小
    """
    st_black = 0
    st_yellow = 0
    end_black = 0
    end_yellow = 0
    for i in range(0, image2.size[0]):
        # width
        ans = 0
        for j in range(image2.size[1]):
            # height
            rgb = image2.load()[i, j]
            if (rgb[0] < 120 and rgb[1] < 120 and rgb[2] < 120):
                # print(i,j,ans,rgb)
                ans = ans + 1
            if (ans > 10):
                st_black = i
                print("st_black:", st_black)
                break
        if st_black > 0:
            break

    for i in range(st_black, image2.size[0]):
        ans = 0
        for j in range(image2.size[1]):
            # height
            rgb = image2.load()[i, j]
            if (rgb[0] > 180 and rgb[1] > 180 and rgb[2] < 200):
                # print(i,j,ans,rgb)
                ans = ans + 1
            if (ans > 20):
                st_yellow = i
                print("st_yellow:", st_yellow)
                break
        if st_yellow > 0:
            break

    return st_yellow

    for i in range(st_yellow + 45, 0, -1):
        # width
        ans = 0
        for j in range(image2.size[1]):
            # height
            rgb = image2.load()[i, j]
            if (rgb[0] < 120 and rgb[1] < 120 and rgb[2] < 120):
                print(i, j, ans, rgb)
                ans = ans + 1
            if (ans > 15):
                end_black = i
                print("end_black:", end_black)
                break
        if end_black > 0:
            break

    for i in range(end_black, 0, -1):
        ans = 0
        for j in range(image2.size[1]):
            # height
            rgb = image2.load()[i, j]
            if (rgb[0] > 165 and rgb[1] > 165 and rgb[2] < 200):
                # print(i,j,ans,rgb)
                ans = ans + 1
            if (ans > 20):
                end_yellow = i
                print("end_yellow:", end_yellow)
                break
        if end_yellow > 0:
            break

    return st_yellow, end_yellow - st_yellow
def get_gap_right(image1, image2):
    """
    获取缺口左端位置
    :param image1: 不带缺口的图片
    :param image2: 带缺口的图片
    :return: 像素是否相同
    """
    # 缺口在滑块右侧，设定遍历初始横坐标left为60
    left = 60
    # 像素对比阈值
    threshold = 50
    for i in range(image1.size[0] - 1, left, -1):
        # width
        ans = 0
        for j in range(image1.size[1]):
            # height
            rgb1 = image1.load()[i, j]
            rgb2 = image2.load()[i, j]
            # print(rgb1,rgb2) #返回值为red，green，black，255

            res1 = abs(rgb2[0] - rgb1[0])
            res2 = abs(rgb2[1] - rgb1[1])
            res3 = abs(rgb2[2] - rgb1[2])
            if (res1 > threshold or res2 > threshold or res3 > threshold):
                # print(i,j,ans,rgb1,rgb2)
                ans = ans + 1
            if (ans > 15):
                return i - 41  # 返回缺口偏移距离，这里需测试几次
# 获取带缺口图片
unfull_path = 'C:/Users/Y/Desktop/临时文件处理/wa/22.38.19wa.pic1.png'
image1 = Image.open(unfull_path)
# 获取完整验证码图片
full_path = 'C:/Users/Y/Desktop/临时文件处理/wa/22.38.19wa.pic2.png'
image2 = Image.open(full_path)
st=get_gap_left(image1)
ed=get_gap_right(image1,image2)
distance = ed-st
print("滑块位置",st)
print("缺口位置",ed)
print("缺口距离",distance)