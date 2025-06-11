import tkinter
from PIL import Image, ImageTk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import filedialog
from cryptography.fernet import Fernet

note = tkinter.Tk()
note.title('Notebook')
note.geometry('500x700')
note.resizable(False, False)

img = Image.open("Python Notebook/notebook_cover.png")
img = img.resize((500,700), Image.Resampling.LANCZOS )
img = ImageTk.PhotoImage(img)

canvas = tkinter.Canvas(note, width=500, height=700)
canvas.create_image(0,0, image=img, anchor='nw')
canvas.pack(fill="both", expand=True)


name_label = tkinter.Label(note, text="Name", bg="#2F4F3E", fg="white")
name_entry = tkinter.Entry(note)

password_label = tkinter.Label(note, text="Password",  bg="#2F4F3E", fg="white")
password_entry = tkinter.Entry(note, show="*")


#Not defteri ekranı
notepad_frame = tkinter.Frame(note)
text_area= tkinter.Text(notepad_frame, wrap="word", font=("Arial",12))
text_area.pack(fill="both", expand=True)



#Kapağa geri dönme butonu
def hide_notepad():
    notepad_frame.pack_forget()
    canvas.pack()    
    hide_menu()
    


#Not defteri kaydetme sistemi
def save_note():
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt")]
    )
    if file_path:
        with open(file_path, "w", encoding="utf-8") as file:
            content = text_area.get(1.0, "end-1c")
            file.write(content)

def open_note():
    file_path = filedialog.askopenfilename(
        filetypes=[("Text Files", "*.txt")]
    )
    if file_path:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            text_area.delete(1.0, "end")
            text_area.insert("end", content)


# Menü çubuğu oluştur
def show_menu():

 menu_bar = tkinter.Menu(note)
 note.config(menu=menu_bar)

# File menüsü
 file_menu = tkinter.Menu(menu_bar, tearoff=0)
 menu_bar.add_cascade(label="File", menu=file_menu)
 file_menu.add_command(label="Open", command=open_note)
 file_menu.add_command(label="Save", command=save_note)
 file_menu.add_separator()
 file_menu.add_command(label="Exit", command=note.quit)

#Menü çubuğunu sakla
def hide_menu():
    note.config(menu="")


try_again_button_id = None
error_message_id = None
name_label_id = None
name_entry_id = None
password_label_id = None
password_entry_id = None
login_button_id = None


#Notebook giriş kontrolü
def check_login():

    global error_message_id, try_again_button_id

    name = name_entry.get()
    password = password_entry.get()

    if name == "Can" and password == "1234":
        canvas.pack_forget()
        notepad_frame.pack(fill="both", expand=True)
        show_menu()
    else:
        # Eski giriş elemanlarını sil
        canvas.delete(name_label_id)
        canvas.delete(name_entry_id)
        canvas.delete(password_label_id)
        canvas.delete(password_entry_id)
        canvas.delete(login_button_id)

        # Hata mesajı oluştur ve ekrana yerleştir
        error_message = tkinter.Label(note, text="⚠ Name or Password Wrong!", fg="red", bg="white", font=("Arial", 12, "bold"))
        error_message_id = canvas.create_window(280, 390, window=error_message)

        try_again_button = tkinter.Button(note, text="Try Again", command=restart_login)
        try_again_button_id = canvas.create_window(280, 420, window= try_again_button)



login_button = tkinter.Button(note, text="Click through to open the notebook",
    bg="#2F4F3E", fg="white", relief="ridge",command=check_login)

login_button_id = canvas.create_window(278, 540, window=login_button)

name_label_id = canvas.create_window(275, 380, window=name_label)
name_entry_id = canvas.create_window(275, 410, window=name_entry)

password_label_id = canvas.create_window(275, 450, window=password_label)
password_entry_id =canvas.create_window(275, 480, window=password_entry)


#Yanlış girişte geri dönme butonu
def restart_login():
 global error_message_id, try_again_button_id, name_label_id, name_entry_id, password_label_id, password_entry_id, login_button_id

 canvas.delete(error_message_id)
 canvas.delete(try_again_button_id)
 
 name_label_id = canvas.create_window(275, 380, window=name_label)
 name_entry_id = canvas.create_window(275, 410, window=name_entry)

 password_label_id = canvas.create_window(275, 450, window=password_label)
 password_entry_id =canvas.create_window(275, 480, window=password_entry)

 login_button_id = canvas.create_window(278, 540, window=login_button)



back_button = tkinter.Button(notepad_frame, text="Back to the Cover", bg="#2F4F3E", fg="white" 
    ,command=hide_notepad)
back_button.pack(anchor="se")
back_button.config(width=70)



# Şifreleme anahtarı
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Sağ üstte yeni bir çerçeve
encrypt_frame = tkinter.Frame(notepad_frame, bg="#e0e0e0", relief="ridge", bd=2)
encrypt_frame.place(relx=0.7, rely=0.02, relwidth=0.28, relheight=0.25)

encrypt_label = tkinter.Label(encrypt_frame, text="Encrypt Panel", bg="#e0e0e0", font=("Arial", 10, "bold"))
encrypt_label.pack(pady=5)

encrypted_output = tkinter.Text(encrypt_frame, height=5, wrap="word", state="disabled")
encrypted_output.pack(padx=5, pady=5, fill="both", expand=True)


def encrypt_notepad_content():
    content = text_area.get("1.0", "end-1c")
    if content.strip():
        encrypted = cipher_suite.encrypt(content.encode()).decode()
    else:
        encrypted = "[Boş metin]"

    encrypted_output.config(state="normal")
    encrypted_output.delete("1.0", "end")
    encrypted_output.insert("1.0", encrypted)
    encrypted_output.config(state="disabled")

encrypt_button = tkinter.Button(encrypt_frame, text="Encrypt", command=encrypt_notepad_content)
encrypt_button.pack(pady=5)

# 🔓 Decrypt Paneli (Encrypt panelinin altına konumlanır)
decrypt_frame = tkinter.Frame(notepad_frame, bg="#f0f0f0", relief="groove", bd=2)
decrypt_frame.place(x=330, y=200, width=160, height=200)  # Alt alta hizalanır

# Başlık
decrypt_label = tkinter.Label(decrypt_frame, text="Decrypt Panel", bg="#f0f0f0", font=("Arial", 10, "bold"))
decrypt_label.pack(pady=5)

# Şifreli metni gireceğimiz kutu
decrypt_input = tkinter.Text(decrypt_frame, height=4, wrap="word")
decrypt_input.pack(padx=5, pady=(0, 5), fill="both", expand=True)

# Çözülmüş metni gösterecek kutu
decrypted_output = tkinter.Text(decrypt_frame, height=4, wrap="word", state="disabled", bg="#fafafa")
decrypted_output.pack(padx=5, pady=(0, 5), fill="both", expand=True)

# Decrypt fonksiyonu
def decrypt_text():
    encrypted_text = decrypt_input.get("1.0", "end-1c")
    try:
        if encrypted_text.strip():
            decrypted = cipher_suite.decrypt(encrypted_text.encode()).decode()
        else:
            decrypted = "[Boş metin]"
    except Exception as e:
        decrypted = f"[Hata]: {str(e)}"

    decrypted_output.config(state="normal")
    decrypted_output.delete("1.0", "end")
    decrypted_output.insert("1.0", decrypted)
    decrypted_output.config(state="disabled")

# Buton
decrypt_button = tkinter.Button(decrypt_frame, text="Decrypt", command=decrypt_text)
decrypt_button.pack(pady=0.5)



note.mainloop()