from os.path import isfile
from conf import login, keystore_file
from modules.keystore import KeyStore
from gi.repository import Gtk, GLib, GObject

class Gfx(object):
    def __init__(self):
        self.width = 300
        self.height = 400
        self.create_window()

    def create_window(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("glade/login.glade")
        self.builder.add_from_file("glade/main.glade")
        self.builder.connect_signals(self)
        if not isfile(keystore_file):
            self.keystore_password_dialog()

    def add_contact(self, widget):
        self.builder.get_object("editUserNicknameEntry").set_text("")
        self.builder.get_object("editUserPassphraseEntry").set_text("")
        self.builder.get_object("editUserIPEntry").set_text("")
        self.builder.get_object("editUserWindow").show_all()
        return True

    def add_user_to_keystore(self, widget):
        nick = self.builder.get_object("editUserNicknameEntry").get_text()
        if len(nick.replace(" ", "")) == 0:
            self.builder.get_object("editUserWindow").hide()
            return False
        ip = self.builder.get_object("editUserIPEntry").get_text()
        passphrase = self.builder.get_object("editUserPassphraseEntry").get_text()
        self.keystore.add_password(nick, ip, passphrase)
        self.builder.get_object("editUserWindow").hide()
        self.fill_users(self.keystore.get_passes())
        return True

    def hide_edit(self, widget):
        self.builder.get_object("editUserWindow").hide()
        return True
        
    def start(self):
        Gtk.main()

    def on_mainWindow_destroy(self, widget):
        Gtk.main_quit()

    def keystore_password_dialog(self):
        self.builder.get_object("keystoreDialog").show()

    def create_keystore(self, widget):
        if self.builder.get_object("keystorePasswordEntry").get_text_length() < 2:
            self.builder.get_object("keystorePasswordNotificationLabel").set_markup("<b>You must use a longer password</b>")
            return False
        self.keystore = KeyStore(keystore_file)
        self.keystore.build(self.builder.get_object("keystorePasswordEntry").get_text())
        self.builder.get_object("keystoreDialog").hide()
        return True

    def edit_user(self, wiget, *data):
        data = data[0]
        self.builder.get_object("editUserWindow").show()
        if "login" in data.keys():
            self.builder.get_object("editUserNicknameEntry").set_text(data['login'])
        if "ip" in data.keys():
            self.builder.get_object("editUserIPEntry").set_text(data['ip'])
        if "password" in data.keys():
            self.builder.get_object("editUserPassphraseEntry").set_text(data['password'])
        return True
        
    def fill_users(self, users):
        grid = self.builder.get_object("usersGrid")
        for index, user in enumerate(users):
            grid.attach(Gtk.Button(label=user['login'], relief=Gtk.ReliefStyle.NONE), 0, index + 1, 1, 1)
            passButton = Gtk.Button(stock=Gtk.STOCK_ADD)
            ipButton = Gtk.Button(stock=Gtk.STOCK_ADD)
            if "password" in user.keys() and len(user['password']) > 0:
                passButton = Gtk.Button(stock=Gtk.STOCK_EDIT, relief=Gtk.ReliefStyle.NONE)
            if "ip" in user.keys() and len(user['ip']) > 0:
                ipButton = Gtk.Button(label=user['ip'], relief=Gtk.ReliefStyle.NONE)
            passButton.connect("clicked", self.edit_user, user)
            ipButton.connect("clicked", self.edit_user, user)
            grid.attach(passButton, 1, index + 1, 1, 1)
            grid.attach(ipButton, 2, index + 1, 1, 1)
        self.builder.get_object("mainWindow").show_all()
        return True
        
    def login_click(self, widget):
        self.pwd_entry = self.builder.get_object("passEntry")
        self.login_entry = self.builder.get_object("loginEntry")
        self.login_notif = self.builder.get_object("loginNotification")
        if self.pwd_entry.get_text_length() < 1:
            self.login_notif.set_markup('<b><span foreground="red" size="large">Invalid Password</span></b>')
            return False
        if self.login_entry.get_text_length() < 1:
            self.login_notif.set_markup('<b><span foreground="red" size="large">Invalid Login</span></b>')
            return False
        self.keystore = KeyStore(keystore_file)
        users = self.keystore.get_passes(self.pwd_entry.get_text())
        if users is None:
            self.login_notif.set_markup('<b><span foreground="red" size="large">KeyStore Password is invalid</span></b>')
            return False
        self.builder.get_object("loginWindow").hide()
        self.builder.get_object("mainWindow").show_all()
        self.builder.connect_signals(self)
        self.fill_users(users)
        return True

    def stop(self):
        Gtk.main_quit()
