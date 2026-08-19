import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from yt_dlp import YoutubeDL

class DownloaderApp(App):
    def build(self):
        self.title = "Video Downloader"
        root = BoxLayout(orientation='vertical', padding=15, spacing=15)
        
        # অ্যাপের হেডার
        title_lbl = Label(text="[b]Standalone Video Downloader[/b]", markup=True, size_hint_y=None, height=40, font_size=20)
        root.add_widget(title_lbl)
        
        # লিংক ইনপুট বক্স
        self.url_input = TextInput(hint_text='Paste YouTube / Facebook / Insta Link here...', size_hint_y=None, height=50)
        root.add_widget(self.url_input)
        
        # ফেচ বাটন
        fetch_btn = Button(text='Get Video Info & Sizes', size_hint_y=None, height=50, background_color=(0.1, 0.6, 0.3, 1))
        fetch_btn.bind(on_press=self.fetch_info)
        root.add_widget(fetch_btn)
        
        # রেজাল্ট দেখানোর লেআউট (স্ক্রোলযোগ্য)
        self.result_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10)
        self.result_layout.bind(minimum_height=self.result_layout.setter('height'))
        
        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(self.result_layout)
        root.add_widget(scroll)
        
        return root

    def fetch_info(self, instance):
        url = self.url_input.text.strip()
        self.result_layout.clear_widgets()
        
        if not url:
            self.result_layout.add_widget(Label(text="Please enter a valid URL!", size_hint_y=None, height=40))
            return
        
        loading_lbl = Label(text="Fetching details and sizes...", size_hint_y=None, height=40)
        self.result_layout.add_widget(loading_lbl)
        
        try:
            ydl_opts = {'noplaylist': True}
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                title = info.get('title', 'Video')
                formats = info.get('formats', [])
                
                self.result_layout.clear_widgets()
                self.result_layout.add_widget(Label(text=f"[b]Title:[/b] {title[:40]}...", markup=True, size_hint_y=None, height=40))
                
                found = False
                for f in formats:
                    # নির্দিষ্ট কোয়ালিটি এবং ফাইল সাইজ ফিল্টার করা
                    if f.get('filesize') and f.get('height') in [360, 720, 1080]:
                        size_mb = round(f['filesize'] / (1024 * 1024), 2)
                        fmt_id = f['format_id']
                        height = f['height']
                        
                        btn_text = f"Download {height}p ({size_mb} MB)"
                        dl_btn = Button(text=btn_text, size_hint_y=None, height=50, background_color=(0.2, 0.4, 0.8, 1))
                        dl_btn.bind(on_press=lambda x, fid=fmt_id, u=url: self.download_video(fid, u))
                        self.result_layout.add_widget(dl_btn)
                        found = True
                
                if not found:
                    self.result_layout.add_widget(Label(text="No direct formats found for this link.", size_hint_y=None, height=40))
        except Exception as e:
            self.result_layout.clear_widgets()
            self.result_layout.add_widget(Label(text=f"Error: {str(e)[:60]}", size_hint_y=None, height=40))

    def download_video(self, fmt_id, url):
        # ফোনের ইন্টারনাল স্টোরেজের Download ফোল্ডারে সেভ করার পাথ
        download_path = '/sdcard/Download/%(title)s.%(ext)s'
        ydl_opts = {
            'format': fmt_id,
            'outtmpl': download_path,
        }
        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            print("Download Completed!")
        except Exception as e:
            print(f"Download Error: {e}")

if __name__ == '__main__':
    DownloaderApp().run()
