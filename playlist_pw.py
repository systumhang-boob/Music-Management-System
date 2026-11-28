# Music Playlist Manager (PBL)
# Concepts used: Lists, Dictionaries, Object-Oriented Programming,
# Random Module, File I/O

import random

FILE = "playlists.txt"


# ---------- Song class ----------
class Song:
    def __init__(self, title, artist, album, duration, genre):
        self.title = title
        self.artist = artist
        self.album = album
        self.duration = duration  # in seconds
        self.genre = genre

    def details(self):
        mins = self.duration // 60
        secs = self.duration % 60
        return f"{self.title} | {self.artist} | {self.album} | {mins}:{secs:02d} | {self.genre}"


# ---------- Data ----------
playlists = {}  # dictionary: playlist name -> list of Song objects
history = []    # list of songs played


# ---------- File I/O (plain text file) ----------
# File format, one item per line, fields separated by "|":
#   PLAYLIST|name
#   SONG|title|artist|album|duration_in_seconds|genre
#   HISTORY|title
def save():
    f = open(FILE, "w")
    for name, songs in playlists.items():
        f.write("PLAYLIST|" + name + "\n")
        for song in songs:
            f.write("SONG|" + song.title + "|" + song.artist + "|" + song.album + "|" + str(song.duration) + "|" + song.genre + "\n")
    for title in history:
        f.write("HISTORY|" + title + "\n")
    f.close()


def load():
    try:
        f = open(FILE, "r")
        current = ""
        for line in f:
            line = line.strip()
            if line == "":
                continue
            parts = line.split("|")
            if parts[0] == "PLAYLIST":
                current = parts[1]
                playlists[current] = []
            elif parts[0] == "SONG":
                playlists[current].append(Song(parts[1], parts[2], parts[3], int(parts[4]), parts[5]))
            elif parts[0] == "HISTORY":
                history.append(parts[1])
        f.close()
    except FileNotFoundError:
        pass  # first run, no file yet
    except (ValueError, IndexError, KeyError):
        print("Save file is damaged. Some data may be missing.")


def clean(text):
    # "|" is used to separate fields in the file, so don't allow it in names
    return text.replace("|", "-")
def show(name):
    if len(playlists[name]) == 0:
        print("  (empty)")
    i = 1
    for song in playlists[name]:
        print(f"  {i}. {song.details()}")
        i = i + 1


def ask_playlist(prompt="Playlist name: "):
    name = input(prompt)
    if name not in playlists:
        print("No such playlist!")
        return None
    return name


def find_song(name, title):
    for song in playlists[name]:
        if song.title.lower() == title.lower():
            return song
    return None


# ---------- Features ----------
def add_song():
    name = ask_playlist()
    if name is None:
        return
    title = clean(input("Title: "))
    artist = clean(input("Artist: "))
    album = clean(input("Album: "))
    try:
        mins = int(input("Duration - minutes: "))
        secs = int(input("Duration - seconds: "))
    except ValueError:
        print("Duration must be a number!")
        return
    genre = clean(input("Genre: "))
    playlists[name].append(Song(title, artist, album, mins * 60 + secs, genre))
    print("Song added!")


def move_or_copy(move):
    src = ask_playlist("From playlist: ")
    if src is None:
        return
    dest = ask_playlist("To playlist: ")
    if dest is None:
        return
    if src == dest:
        print("Both playlists are the same!")
        return
    song = find_song(src, input("Song title: "))
    if song is None:
        print("Song not found!")
        return
    playlists[dest].append(song)
    if move:
        playlists[src].remove(song)
        print("Song moved!")
    else:
        print("Song copied!")


def sort_playlist():
    name = ask_playlist()
    if name is None:
        return
    choice = input("Sort by (title/artist/duration): ").lower()
    if choice == "title":
        playlists[name].sort(key=lambda s: s.title.lower())
    elif choice == "artist":
        playlists[name].sort(key=lambda s: s.artist.lower())
    elif choice == "duration":
        playlists[name].sort(key=lambda s: s.duration)
    else:
        print("Invalid choice!")
        return
    show(name)


def total_duration():
    name = ask_playlist()
    if name is None:
        return
    total_secs = 0
    for song in playlists[name]:
        total_secs = total_secs + song.duration
    hours = total_secs // 3600
    minutes = (total_secs % 3600) // 60
    print(f"Total duration: {hours} hour(s) {minutes} minute(s)")


def search():
    word = input("Search for: ").lower()
    found = False
    for name, songs in playlists.items():
        for song in songs:
            if word in song.details().lower():
                print(f"  [{name}] {song.details()}")
                found = True
    if not found:
        print("No songs found.")


def play():
    name = ask_playlist()
    if name is None:
        return
    title = input("Song to play (press Enter to play whole playlist): ")
    if title == "":
        for song in playlists[name]:
            print("  Playing:", song.title)
            history.append(song.title)
    else:
        song = find_song(name, title)
        if song is None:
            print("Song not found!")
        else:
            print("  Playing:", song.title)
            history.append(song.title)


def menu():
    print("\n===== PLAYLIST MANAGER =====")
    print("1. Create playlist       8. Shuffle playlist")
    print("2. Rename playlist       9. Sort playlist")
    print("3. Delete playlist      10. Total duration")
    print("4. Add song             11. Search songs")
    print("5. View playlist        12. Play song")
    print("6. Move song            13. Playback history")
    print("7. Copy song             0. Exit")


# ---------- Main program ----------
def main():
    load()
    while True:
        menu()
        choice = input("Choose: ")

        if choice == "1":
            name = clean(input("New playlist name: "))
            if name in playlists:
                print("Already exists!")
            else:
                playlists[name] = []
                print("Playlist created!")
        elif choice == "2":
            old = ask_playlist("Old name: ")
            if old is not None:
                new = clean(input("New name: "))
                if new in playlists:
                    print("That name is already used!")
                else:
                    playlists[new] = playlists[old]
                    del playlists[old]
                    print("Renamed!")
        elif choice == "3":
            name = ask_playlist()
            if name is not None:
                del playlists[name]
                print("Deleted!")
        elif choice == "4":
            add_song()
        elif choice == "5":
            name = ask_playlist()
            if name is not None:
                show(name)
        elif choice == "6":
            move_or_copy(True)
        elif choice == "7":
            move_or_copy(False)
        elif choice == "8":
            name = ask_playlist()
            if name is not None:
                random.shuffle(playlists[name])
                show(name)
        elif choice == "9":
            sort_playlist()
        elif choice == "10":
            total_duration()
        elif choice == "11":
            search()
        elif choice == "12":
            play()
        elif choice == "13":
            if len(history) == 0:
                print("Nothing played yet.")
            for title in history:
                print("  -", title)
        elif choice == "0":
            save()
            print("Saved. Bye!")
            break
        else:
            print("Invalid choice!")

        save()


main()
