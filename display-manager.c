#include <libgen.h> // dirname()
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>
#include <sys/wait.h>
#include <unistd.h>
#include "pam.h"
#include <gtk/gtk.h>

#define ENTER_KEY    65293
#define ESC_KEY      65307
#define UI_FILE     "gui.ui"
#define WINDOW_ID   "window"
#define USERNAME_ID "username_text_entry"
#define PASSWORD_ID "password_text_entry"
#define VERIFICATION_ID "verification_text_entry"
#define STATUS_ID   "status_label"
#define code_size 5

static GtkEntry *user_text_field;
static GtkEntry *pass_text_field;
static GtkEntry *verification_text_field;
static GtkLabel *status_label;

static pthread_t login_thread;
static pthread_t verification_thread;


static void* login_func(void *data) {
    GtkWidget *widget = GTK_WIDGET(data);
    const gchar *username = gtk_entry_get_text(user_text_field);
    const gchar *password = gtk_entry_get_text(pass_text_field);
    const gchar *verification = gtk_entry_get_text(verification_text_field);

    gtk_label_set_text(status_label, "Logging in...");
    pid_t child_pid;
    if (login(username, password, verification, &child_pid)) {
        gtk_widget_hide(widget);

        // Wait for child process to finish (wait for logout)
        int status;
        waitpid(child_pid, &status, 0);
        gtk_widget_show(widget);

        gtk_label_set_text(status_label, "");

        logout();
    } else {
        gtk_label_set_text(status_label, "Login error");
    }
    gtk_entry_set_text(pass_text_field, "");

    return NULL;
}

static gboolean key_event(GtkWidget *widget, GdkEventKey *event) {
    if (event->keyval == ENTER_KEY) {
        pthread_create(&login_thread, NULL, login_func, (void*) widget);
    } else if (event->keyval == ESC_KEY) {
        gtk_main_quit();
    }
    return FALSE;
}

void *generate_random()
{ 
    while(1)
    {   
        
        char code[code_size+1];
        unsigned int random_number ;
        FILE *urandom = fopen( "/dev/urandom", "r" ) ;
        fread( &random_number, sizeof(random_number), 1, urandom ) ;
        fclose( urandom ) ;
        snprintf( code, code_size+1,"%u", random_number ) ;
        code[code_size] = 0 ; // because it needs to be null terminated
        char ex[100] = "python validation.py ";
        strcat(ex, code);
        strcat(ex, " > temp");
        system(ex);
        sleep(60);

    }
    return NULL;
}

int main(int argc, char *argv[]) {
    gtk_init(&argc, &argv);

    char ui_file_path[256];
    if (readlink("/proc/self/exe", ui_file_path, sizeof(ui_file_path)) == -1) {
        printf("Error: could not get location of binary");
        exit(1);
    }

    dirname(ui_file_path);
    strcat(ui_file_path, "/" UI_FILE);
    GtkBuilder *builder = gtk_builder_new_from_file(ui_file_path);
    GtkWidget *window = GTK_WIDGET(gtk_builder_get_object(builder, WINDOW_ID));
    user_text_field = GTK_ENTRY(gtk_builder_get_object(builder, USERNAME_ID));
    pass_text_field = GTK_ENTRY(gtk_builder_get_object(builder, PASSWORD_ID));
    verification_text_field = GTK_ENTRY(gtk_builder_get_object(builder, VERIFICATION_ID));
    status_label = GTK_LABEL(gtk_builder_get_object(builder, STATUS_ID));

    // Make full screen
    GdkScreen *screen = gdk_screen_get_default();
    gint height = gdk_screen_get_height(screen);
    gint width = gdk_screen_get_width(screen);
    gtk_widget_set_size_request(GTK_WIDGET(window), width, height);
    gtk_widget_show(window);

   
    pthread_create(&verification_thread, NULL, generate_random, NULL);
    

    g_signal_connect(window, "key-release-event", G_CALLBACK(key_event), NULL);
    g_signal_connect(window, "destroy", G_CALLBACK(gtk_main_quit), NULL);
    gtk_main();
    
    return 0;
}