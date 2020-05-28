import random
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
import time
import os
from selenium import webdriver
from PIL import Image #获取图像RGB值
import easing

class CrackGreetest():
    def __init__(self):
        self.url = "https://auth.geetest.com/login/"
        self.browser = webdriver.Chrome(executable_path = 'D:\\2019Download\\ChromeDriver\\chromedriver.exe')
        self.wait = WebDriverWait(self.browser,20)
        self.email = 'youremail@email.com'

    def open(self):
        """
    	打开网页输入用户名密码
    	:return:
    	"""
        self.browser.get(self.url)
        email = self.wait.until(expected_conditions.presence_of_element_located((By.CLASS_NAME,'ivu-input')))
        # password = self.wait.until(expected_conditions.presence_of_element_located((By.ID,'password')))
        email.send_keys(self.email)
        # password.send_keys(self.password)

    def get_geetest_button(self):
        '''
        获取初始验证码按钮
        :return: 按钮对象
        '''
        button = self.wait.until(expected_conditions.element_to_be_clickable((By.CLASS_NAME,'geetest_radar_tip')))
        return button

    def get_unfull_image(self, path):
        """
        获取未完整验证码图片
        :param name:
        :return: 图片对象
        """
        element = self.browser.find_element_by_css_selector(
            "body > div.geetest_fullpage_click.geetest_float.geetest_wind.geetest_slide3 > div.geetest_fullpage_click_wrap > div.geetest_fullpage_click_box > div > div.geetest_wrap > div.geetest_widget > div > a > div.geetest_canvas_img.geetest_absolute > div > canvas.geetest_canvas_slice.geetest_absolute")

        unfull_captcha = element.screenshot(path)
        return unfull_captcha

    def get_full_image(self,path):
        '''
        获取完整验证码图片
        :param name:
        :return:
        '''
        # 这里要执行JavaScript脚本才能拿到完整图片的截图
        show_Full_img1 = "document.getElementsByClassName('geetest_canvas_fullbg')[0].style.display='block'"
        self.browser.execute_script(show_Full_img1)
        show_Full_img2 = "document.getElementsByClassName('geetest_canvas_fullbg')[0].style.opacity=1"
        self.browser.execute_script(show_Full_img2)
        # 等待完整图片加载
        time.sleep(2)
        element = self.browser.find_element_by_css_selector(
            "body > div.geetest_fullpage_click.geetest_float.geetest_wind.geetest_slide3 > div.geetest_fullpage_click_wrap > div.geetest_fullpage_click_box > div > div.geetest_wrap > div.geetest_widget > div > a > div.geetest_canvas_img.geetest_absolute > canvas")
        full_captcha = element.screenshot(path)
        return full_captcha

    def get_slider(self):
        """
        获取滑块
        :return: 滑块对象
        """
        slider = self.wait.until(expected_conditions.element_to_be_clickable((By.CLASS_NAME,'geetest_slider_button')))
        return slider

    def get_gap_left(self,image2):
        """
        获取滑块左端位置及滑块大小
        :param image2: 带缺口的图片
        :return: 滑块左端位置，滑块大小
        """
        st_black = 0
        st_yellow=0
        end_black=0
        end_yellow=0
        for i in range(0,image2.size[0]):
            #width
            ans=0
            for j in range(image2.size[1]):
                #height
                rgb = image2.load()[i, j]
                if  ( rgb[0]<120 and rgb[1] < 120 and rgb[2] <120):
                    ans=ans+1
                if(ans>10):
                    st_black = i
                    break
            if st_black>0:
                break

        for i in range(st_black,image2.size[0]):
            ans=0
            for j in range(image2.size[1]):
                #height
                rgb = image2.load()[i, j]
                if  ( rgb[0]>180 and rgb[1] > 180 and rgb[2] <200):
                    ans=ans+1
                if(ans>20):
                    st_yellow=i
                    break
            if st_yellow>0:
                break

        return st_yellow

        #暂时弃置
        for i in range(st_yellow+45,0,-1):
            #width
            ans=0
            for j in range(image2.size[1]):
                #height
                rgb = image2.load()[i, j]
                if  ( rgb[0]<120 and rgb[1] < 120 and rgb[2] <120):
                    ans=ans+1
                if(ans>15):
                    end_black = i
                    break
            if end_black>0:
                break

        for i in range(end_black,0,-1):
            ans=0
            for j in range(image2.size[1]):
                #height
                rgb = image2.load()[i, j]
                if  ( rgb[0]>165 and rgb[1] >165 and rgb[2] <200):
                    ans=ans+1
                if(ans>20):
                    end_yellow = i
                    break
            if end_yellow>0:
                break

        return st_yellow,end_yellow-st_yellow

    def get_gap_right(self,image1,image2):
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
        for i in range(image1.size[0]-1, left, -1):
            #width
            ans=0
            for j in range(image1.size[1]):
                #height
                rgb1 = image1.load()[i, j]
                rgb2 = image2.load()[i, j]

                res1 = abs(rgb2[0] - rgb1[0])
                res2 = abs(rgb2[1] - rgb1[1])
                res3 = abs(rgb2[2] - rgb1[2])
                if  (res1 > threshold or res2 > threshold or res3 > threshold):
                    ans=ans+1
                if(ans>15):
                    return i-41  # 返回缺口偏移距离，这里需测试几次


    def move_to_grap(self,slider,distance,paring):
        '''
        拖动滑块到缺口处
        :param slider: 滑块
        :param track: 轨迹
        :return:
        '''
        ans=random.randint(3,4)
        offsets, track = easing.get_tracks(distance, ans*2, paring)
        # print(offsets)
        # 调用ActionChains的click_and_hold()方法按住拖动底部滑块，遍历运动轨迹获取每小段位置距离，调用move_by_offset()方法移动此位移，最后调用release()方法松开鼠标
        ActionChains(self.browser).click_and_hold(slider).perform()
        for x in track:
            ActionChains(self.browser).move_by_offset(xoffset=x,yoffset=0).perform()
            time.sleep(0.01)
        time.sleep(0.3)
        ActionChains(self.browser).release().perform()

    def crack(self,paring):
        try:
            # 输入用户名
            self.open()

            # 模拟点击按钮
            button = self.get_geetest_button()
            button.click()
            time.sleep(2)

            tn=time.localtime(time.time())

            # 获取带缺口验证码图片
            unfull_path = 'D:\Documents\Desktop\TempHandle/ans/'+str(tn.tm_mday)+'.'+str(tn.tm_min)+'.'+str(tn.tm_sec)+'pic1.png'
            self.get_unfull_image(unfull_path)
            image1 = Image.open(unfull_path)

            # 获取完整的验证码图片
            full_path = 'D:\Documents\Desktop\TempHandle/ans/'+str(tn.tm_mday)+'.'+str(tn.tm_min)+'.'+str(tn.tm_sec)+'pic2.png'
            self.get_full_image(full_path)
            image2 = Image.open(full_path)
            #
            # 对比两张图片像素点，获取缺口位置，得到偏移距离
            # 获取缺口位置
            st=self.get_gap_left(image1)
            ed=self.get_gap_right(image1,image2)
            distance = ed-st
            # print("缺口距离",distance)

            # # 获取移动轨迹
            # track = self.get_track(distance)
            # print("滑动轨迹",track)

            # 模拟人的行为，拖动滑块，完成验证
            slider = self.get_slider()
            # slider.click()

            # 拖动滑块
            self.move_to_grap(slider, distance, paring)
            time.sleep(1)
            text=self.browser.find_element_by_class_name('geetest_result_title').get_attribute('textContent')

            return

            # if(text=='哇哦～怪物吃了拼图请 3 秒后重试'):
            #     res[1]+=1
            #     return
            # elif(text=='拖动滑块将悬浮图像正确拼合'):
            #     res[2]+=1
            #     return
            # else:
            #     #text=='sec 秒的速度超过 score% 的用户'
            #     res[0]+=1
            #     return
        except:
            return

if __name__ == "__main__":
    crack = CrackGreetest()

    parameter=['ease_in_out_quad','ease_out_cubic','ease_in_out_cubic','ease_out_quart',
               'ease_in_out_quart','ease_out_quint','ease_in_out_quint','ease_out_sine',
               'ease_in_out_sine','ease_out_expo','ease_in_out_expo','ease_out_cric',
               'ease_in_out_cric','ease_out_elastic','ease_out_back','ease_in_out_back']

    while(True):
        ans=random.randint(0,15)
        crack.crack( parameter[ans])

    # for par in parameter:
    #     print(par)
    #     res1 = [0, 0, 0]
    #     res2 = [0, 0, 0]
    #     t1 = 100
    #     t2 = 100
    #     for i in range(t1):
    #         ans = crack.crack(res1,par)
    #         # print(i)
    #     for i in range(t2):
    #         ans = crack.crack(res2,par)
    #         # print(i)
    #     # print('共测试了t1',t1,'次')
    #     print('成功了',res1[0],'次')
    #     print('被吃掉',res1[1],'次')
    #     print('位置错误',res1[2],'次')
    #     # print('共测试了t2',t2,'次')
    #     print('成功了',res2[0],'次')
    #     print('被吃掉',res2[1],'次')
    #     print('位置错误',res2[2],'次')
