import time

import requests
from bs4 import BeautifulSoup


class get6MinsEnglish:
    def __init__(self):
        self.infos = []

        # 目标网址
        url = "https://www.bbc.co.uk/learningenglish/english/features/6-minute-english"

        # 发送 GET 请求获取网页内容
        response = requests.get(url)
        response.raise_for_status()  # 确保请求成功

        # 使用 BeautifulSoup 解析 HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # 找到所有节目条目
        episodes = soup.find_all('li', class_='course-content-item active')
        # print(episodes)
        # 遍历每个节目，提取链接、标题和发布时间
        for episode in episodes:
            title = episode.find('h2').find('a').get_text(strip=True)
            link = episode.find('a')['href']
            publish_date = episode.find('b')

            # 获取发布时间，如果没有找到则为空
            if publish_date:
                publish_date = publish_date.get_text(strip=True)
            else:
                publish_date = "未知"
            self.infos.append([publish_date, title, "https://www.bbc.co.uk" + link])
            # print(f"标题: {title}")
            # print(f"链接: https://www.bbc.co.uk{link}")
            # print(f"发布时间: {publish_date}")
            # print("-" * 40)

    def downloadTrascripts(self):
        for info in self.infos:
            # infos的最后一个是url
            temp_url = info[-1]

            # 网站240516后修改了版面使用新方法获取
            if int(info[0].split(" ")[-1]) > 181129:
                # response = requests.get(temp_url)
                # response.raise_for_status()
                # soup = BeautifulSoup(response.text, 'html.parser')
                # trs = soup.find_all('div', class_='widget widget-richtext 6')
                # links = trs[0].find_all('h3')
                # pdf_url = links[1].find('a')['href']
                # print("downloads pdf:", links[1].find('a')['href'])
                # self.downloadFiles(pdf_url, info[0] + "-" +info[1], "pdf")
                # time.sleep(2)
                pass
            else:
                print(temp_url)
                response = requests.get(temp_url)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                trs = soup.find_all('div', class_='widget-container widget-container-right')
                print(trs)
                links = trs[0].find('div').find_all('a')
                for link in links:
                    print(link['href'])
                if len(links)>1:
                    pdf_url = links[0]['href']
                    mp3_url = links[1]['href']
                    print("pdf_url", pdf_url)
                    print("mp3_url", mp3_url)
                    self.downloadFiles(pdf_url, info[0] + "-" +info[1],"pdf")
                    time.sleep(1)
                    self.downloadFiles(mp3_url, info[0] + "-" +info[1],"mp3")
                    time.sleep(1)


    def downloadFiles(self, url, file_name, file_type):
        import re
        # 定义非法字符
        invalid_chars = r'[<>:"/\\|?*]'
        # 使用正则替换非法字符
        clean_filename = re.sub(invalid_chars, "", file_name)

        if file_type == "pdf":
            # 发送 GET 请求下载文件
            response = requests.get(url)
            # 检查请求是否成功
            if response.status_code == 200:
                # 获取文件的内容
                file_content = response.content
                file_save_dir = "./transcript_pdf/" + clean_filename + ".pdf"
                with open(file_save_dir, 'wb') as file:
                    file.write(file_content)
                    print(f"文件下载成功，保存为 {file_save_dir}")
            else:
                print(f"下载失败，状态码: {response.status_code}")
        else:
            # 设置保存音频的文件名
            file_save_dir = "./transcript_mp3/" + clean_filename + ".mp3"
            # 选择保存的路径和文件名
            # 下载音频文件
            audio_response = requests.get(url, stream=True)
            # 检查请求是否成功
            if audio_response.status_code == 200:
                # 设置保存文件的路径和文件名
                # 将文件写入本地
                with open(file_save_dir, 'wb') as file:
                    for chunk in audio_response.iter_content(chunk_size=8192):  # 分块写入文件
                        file.write(chunk)

                print(f"文件下载成功，保存为 {file_save_dir}")
            else:
                print(f"下载失败，状态码: {audio_response.status_code}")



if __name__ == '__main__':
    mainclass = get6MinsEnglish()
    mainclass.downloadTrascripts()