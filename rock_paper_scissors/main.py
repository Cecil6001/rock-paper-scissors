import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk
import cv2
from hand_recognition import HandRecognition
from game_logic import GameLogic
import os
class RockPaperScissorsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Rock-Paper-Scissors Game")
        self.root.geometry("800x600")

        # 手势识别和游戏逻辑模块
        self.hand_recognition = HandRecognition()
        self.game_logic = GameLogic()
        self.camera = cv2.VideoCapture(0)

        if not self.camera.isOpened():
            raise ValueError("无法打开摄像头，请检查摄像头连接。")

        # 初始化玩家和电脑的手势
        self.player_hand = "unknown"
        self.computer_hand = "unknown"

        # 资源路径
        self.assets_path = "./assets/"
        if not os.path.exists(self.assets_path):
            raise ValueError(f"资源路径 {self.assets_path} 不存在。请确保图片文件夹存在。")

        # 摄像头显示
        self.video_label = Label(root)
        self.video_label.pack(pady=10)

        # 玩家手势显示
        self.player_label = Label(root, text="Player's move: ", font=("Arial", 18))
        self.player_label.pack()

        # 玩家手势图片
        self.player_image_label = Label(root)
        self.player_image_label.pack(pady=5)

        # 电脑手势显示
        self.computer_label = Label(root, text="Computer's move: ", font=("Arial", 18))
        self.computer_label.pack()

        # 电脑手势图片
        self.computer_image_label = Label(root)
        self.computer_image_label.pack(pady=5)

        # 游戏结果显示
        self.result_label = Label(root, text="", font=("Arial", 20, "bold"))
        self.result_label.pack(pady=10)

        # 开始更新画面
        self.update_frame()

        # 处理窗口关闭事件，释放摄像头
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def get_hand_image(self, hand_name):
        """根据手势名称获取对应图片"""
        image_path = os.path.join(self.assets_path, f"{hand_name}.png")
        if not os.path.exists(image_path):
            print(f"图片文件 {image_path} 不存在。")
            return None
        try:
            image = Image.open(image_path)
            return ImageTk.PhotoImage(image.resize((100, 100)))
        except Exception as e:
            print(f"加载图片 {image_path} 失败: {e}")
            return None

    def update_frame(self):
        """更新摄像头画面和手势识别"""
        ret, frame = self.camera.read()
        if ret:
            # 检测玩家的手势
            gestures = self.hand_recognition.detect_hand(frame)
            if gestures:
                player_gesture = gestures[0].lower()  # 确保手势名称为小写
                if player_gesture in ["rock", "paper", "scissors"]:
                    self.player_hand = player_gesture
                    self.player_label.config(text=f"Player's move: {self.player_hand.capitalize()}")

                    # 更新玩家手势图片
                    player_img = self.get_hand_image(self.player_hand)
                    if player_img:
                        self.player_image_label.config(image=player_img)
                        self.player_image_label.image = player_img

                    # 生成电脑的手势，确保赢玩家
                    self.computer_hand = self.game_logic.computer_always_win(self.player_hand)
                    self.computer_label.config(text=f"Computer's move: {self.computer_hand.capitalize()}")

                    # 更新电脑手势图片
                    computer_img = self.get_hand_image(self.computer_hand)
                    if computer_img:
                        self.computer_image_label.config(image=computer_img)
                        self.computer_image_label.image = computer_img

                    # 判断结果
                    result = self.game_logic.judge(self.player_hand, self.computer_hand)
                    if result == "win":
                        result_text = "Player Wins!"
                        self.result_label.config(text=result_text, fg="green")
                    elif result == "lose":
                        result_text = "Computer Wins!"
                        self.result_label.config(text=result_text, fg="red")
                    elif result == "draw":
                        result_text = "It's a Draw!"
                        self.result_label.config(text=result_text, fg="blue")
                    else:
                        result_text = "Invalid Move!"
                        self.result_label.config(text=result_text, fg="black")

                    # 打印调试信息
                    print(f"Player: {self.player_hand}, Computer: {self.computer_hand}, Result: {result}")

                else:
                    # 处理未知手势
                    self.player_hand = "unknown"
                    self.player_label.config(text="Player's move: Unknown")
                    self.computer_hand = "unknown"
                    self.computer_label.config(text="Computer's move: Unknown")
                    self.result_label.config(text="", fg="black")
            else:
                # 没有检测到手势
                self.player_hand = "unknown"
                self.player_label.config(text="Player's move: Unknown")
                self.computer_hand = "unknown"
                self.computer_label.config(text="Computer's move: Unknown")
                self.result_label.config(text="", fg="black")

            # 显示摄像头画面
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)

        # 每隔30毫秒更新一次画面
        self.root.after(30, self.update_frame)

    def on_closing(self):
        """关闭应用时释放摄像头资源"""
        if self.camera.isOpened():
            self.camera.release()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = RockPaperScissorsApp(root)
    root.mainloop()
