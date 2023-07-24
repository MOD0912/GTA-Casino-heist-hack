"""
Blackjack.py
13. June 2023

Blackjack Game

Author:
Melvin Kapferer, Maximilian Koch
"""
from PIL import Image, ImageTk
import customtkinter as ctk
from enum import Enum
import random
import sys
import os
import re
import time


# remove not-working auto-dpi awareness
ctk.deactivate_automatic_dpi_awareness()

# enumerators for players / winners
class PlayerKind(Enum):
    player = "Player"
    croupier = "Croupier"


class WinnerKind(Enum):
    player = "Player"
    croupier = "Croupier"
    draw = "Draw"


class Cards:
    """
    Cards
    """
    @staticmethod
    def function() -> list[str]:
        """
        generates a list of all available images in ./cards/
        """
        path = "cards"
        filelist = []
        for root, dirs, files in os.walk(path):
            for file in files:
                if file == "CardBack.png":
                    continue
                filelist.append(os.path.join(root, file))
        return filelist


class BlackjackGame(ctk.CTk):
    second_card_counter: int = ...
    player_cards_x: int = ...
    player_cards_y: int = ...
    croupier_cards_x: int = ...
    croupier_cards_y: int = ...
    x_change: int = ...
    y_change: int = ...
    value_player: int = ...
    value_croupier: int = ...
    lst: list[ImageTk.PhotoImage] = ...
    filelist: list[str] = ...

    bg: ImageTk.PhotoImage = ...
    canvas1: ctk.CTkCanvas = ...
    hit_btn: ctk.CTkButton = ...
    stand_btn: ctk.CTkButton = ...
    leave_btn: ctk.CTkButton = ...

    croupier_text: int = -1
    player_text: int = -1
    hidden_card: int = -1

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.width = self.winfo_screenwidth()
        self.height = self.winfo_screenheight()
        self.playercoins = 300
        self.all_coins = [500, 250, 100, 50, 20, 10]

        # window configuration
        # check if the os is windows, and if not set fullscreen by using
        # root.attributes instead of zoomed (state won't work on linux / darwin
        if sys.platform == "win32":
            self.after(0, lambda: self.state("zoomed"))
        else:
            self.attributes("-zoomed", 1)

        self.attributes("-fullscreen", True)
        self.bg = ImageTk.PhotoImage(
            Image.open("./design/design1.png").resize(
                size=(self.width, self.height)
            )
        )
        self.delet()
        self.create_widgets()
        self.coins()

    def calculatecoins(self, coin):
        '''
        Calculate what coins the player gets
        '''
        print(self.playercoins)
        print(coin)
        print()
        z = 0
        if coin == self.playercoins:
            self.listofcoinst.append(1)
            print(self.listofcoinst)
            print()
            return "jaisNone"
        
        if coin > self.playercoins:
            self.listofcoinst.append(0)
            print(self.listofcoinst)
            print()
            return
        
        while self.playercoins > coin:
            self.playercoins -= coin
            z+=1

        self.listofcoinst.append(z)
        print(self.listofcoinst)
        print()


    def coins(self):
        """
        handles the coins and bets of the game

        Coins: 10, 20, 50, 100, 250, 500
        """
        playercoins = self.playercoins
        self.listofcoinst = []
        self.playercoins
        for i in self.all_coins:
            isNone = self.calculatecoins(i)
            if isNone == "jaisNone":
                break
        self.coincanvas.pack(anchor="sw", side="bottom", pady=200, padx=200)
        self.playercoins = playercoins
        self.coincanvas.create_image(0, 0, image=ImageTk.PhotoImage(Image.open("cards/CardBack.png")))

    def delet(self) -> None:
        """
        resets all values to game start
        """
        self.second_card_counter = 0
        self.player_cards_x = int(self.width / 2)
        self.player_cards_y = int(self.height / 1.479)
        self.croupier_cards_x = int(self.width / 2)
        self.croupier_cards_y = int(self.height / 4.695)
        self.x_change = 20
        self.y_change = 20
        self.value_player = 0
        self.value_croupier = 0
        self.lst = []
        self.filelist = Cards().function()


    def create_widgets(self) -> None:
        """
        creates all the game-widgets
        """
        self.canvas1 = ctk.CTkCanvas(self, border=0, highlightthickness=0)
        self.canvas1.pack(fill="both", expand=True)
        self.canvas1.create_image(0, 0, image=self.bg, anchor="nw")
        self.croupier_text = self.canvas1.create_text(
            self.width / 2,
            self.height / 21.6,
            text=f"croupier value: {self.value_croupier}",
            font=(
                'Times New Roman', 20,
                'bold'
            ),
            fill="white"
        )
        self.player_text = self.canvas1.create_text(
            self.width / 2,
            self.height / 2,
            text=f"croupier value: {self.value_croupier}",
            font=(
                'Times New Roman',
                20,
                'bold'
            ),
            fill="white"
        )
        self.hit_btn = ctk.CTkButton(
            self.canvas1,
            text="Hit",
            height=int(self.height / 21.6),
            width=int(self.width / 9.6),
            command=lambda: self.create_cards(PlayerKind.player),
            fg_color="#202020",
            corner_radius=0
        )
        self.hit_btn.place(
            x=self.width / 2 - self.width / 4.8,
            y=self.height - self.height / 10.8
        )
        self.stand_btn = ctk.CTkButton(
            self.canvas1,
            text="Stand",
            height=int(self.height / 21.6),
            width=int(self.width / 9.6),
            command=self.stand,
            fg_color="#202020",
            corner_radius=0
        )
        self.stand_btn.place(
            x=self.width / 2,
            y=self.height - self.height / 10.8,
            anchor="n"
        )
        self.leave_btn = ctk.CTkButton(
            self.canvas1,
            text="Hit and run",
            height=int(self.height / 21.6),
            width=int(self.width / 9.6),
            command=exit,
            fg_color="#202020",
            corner_radius=0
        )
        self.leave_btn.place(
            x=self.width / 2 + self.width / 4.8,
            y=self.height - self.height / 10.8,
            anchor="ne"
        )
        self.coincanvas = ctk.CTkCanvas(self.canvas1)

        self.create_cards(PlayerKind.player)
        self.create_cards(PlayerKind.croupier)
        self.create_cards(PlayerKind.player)
        self.create_cards(PlayerKind.croupier)

    def create_cards(self, player: PlayerKind) -> None:
        """
        creates one card and places it

        :param player: must be either Player or Croupier
        """
        if len(self.filelist) == 0:
            self.filelist = Cards().function()

        card = random.choice(self.filelist)

        self.filelist.remove(card)
        value = int(
            re.search(r'\d+', card).group()
        )  # gets integer out of a string

        if player == PlayerKind.player:
            self.player_cards_x += self.x_change
            self.player_cards_y += self.y_change
            x = self.player_cards_x - self.x_change
            y = self.player_cards_y - self.y_change
            self.value_player += value
            print(f"player value:{self.value_player}")

        elif player == PlayerKind.croupier:
            self.second_card_counter += 1
            if self.second_card_counter == 2:
                card = "cards/CardBack.png"

            else:
                self.value_croupier += value
            self.croupier_cards_x += self.x_change
            self.croupier_cards_y += self.y_change
            x = self.croupier_cards_x - self.x_change
            y = self.croupier_cards_y - self.y_change

            print(f"croupier value:{self.value_croupier}")

        else:
            raise ValueError("Invalid value for player!")

        self.canvas1.itemconfig(
            self.croupier_text,
            text=f"croupier value: {self.value_croupier}"
        )
        self.canvas1.itemconfig(
            self.player_text,
            text=f"player value: {self.value_player}"
        )
        card = ImageTk.PhotoImage(Image.open(card).resize(
            (int(self.width / 9.6), int(self.height / 3.6)))
        )
        image = self.canvas1.create_image(x, y, image=card)

        if self.second_card_counter == 2 and player == "Croupier":
            self.hidden_card = image
        self.lst.append(card)  # handles common error
        if self.value_player > 21:
            self.end(WinnerKind.croupier)

        elif self.value_croupier > 21:
            self.end(WinnerKind.player)

        if self.value_player == 21:
            self.stand()

    def stand(self) -> None:
        """
        ends the players turn
        """
        self.croupier_cards_x = self.croupier_cards_x - self.x_change
        self.croupier_cards_y = self.croupier_cards_y - self.y_change
        self.canvas1.delete(self.hidden_card)

        while self.value_croupier < 17:
            self.create_cards(PlayerKind.croupier)
            time.sleep(0.5)

        if self.value_croupier < self.value_player:
            winner = WinnerKind.player

        elif self.value_croupier > self.value_player:
            winner = WinnerKind.croupier

        else:
            winner = WinnerKind.draw

        if self.value_croupier > 21 or self.value_player > 21:
            return

        self.end(winner)

    def end(self, winner: WinnerKind) -> None:
        """
        handles the end of a round

        :param winner: the rounds winner
        """
        print(f"winner is {winner}")
        if winner == WinnerKind.draw:
            text = "draw"
            x = 625

        else:
            text = f"{winner.value} won!"

            if winner == WinnerKind.player:
                x = 200
            elif winner == WinnerKind.croupier:
                x = 125
            else:
                raise ValueError("Invalid value for winner")

        self.hit_btn.configure(state="disabled")
        self.stand_btn.configure(state="disabled")
        self.frame_end = ctk.CTkFrame(self, width=500, height=500)
        self.frame_end.place(x=x, y=300)
        label_end = ctk.CTkLabel(
            self.frame_end,
            text=text,
            font=('Times New Roman', 300, 'bold')
        )
        label_end.pack()
        button_end_restart = ctk.CTkButton(
            self.frame_end,
            text="Again?",
            command=self.close,
            height=50
        )
        button_end_restart.pack(fill="x")
        button_end_end = ctk.CTkButton(
            self.frame_end,
            text="End the game",
            command=exit,
            height=50
        )
        button_end_end.pack(fill="x")

    def close(self) -> None:
        """
        restarts the game
        """
        self.hit_btn.configure(state="normal")
        self.stand_btn.configure(state="normal")
        self.frame_end.destroy()
        self.lst.clear()
        print(self.lst)
        self.delet()
        time.sleep(0.1)
        self.create_cards(PlayerKind.player)
        self.create_cards(PlayerKind.croupier)
        self.create_cards(PlayerKind.player)
        self.create_cards(PlayerKind.croupier)



if __name__ == '__main__':
    game = BlackjackGame()
    game.mainloop()
