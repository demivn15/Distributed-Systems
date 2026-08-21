// Server socket in C (Multithreaded)
#include <errno.h>
#include <netdb.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <unistd.h>
#include <pthread.h>
#include <ctype.h>

#define PORT 12000 // Match Python port
#define BACKLOG 10

// Función que ejecutará cada hilo
void *handle_client(void *arg)
{
    int client_fd = *((int *)arg);
    free(arg); // Liberamos la memoria del puntero

    char buffer[BUFSIZ];
    int bytes_read;

    printf("[Thread] Handling client socket %d\n", client_fd);

    while (1)
    {
        bytes_read = recv(client_fd, buffer, BUFSIZ - 1, 0);
        if (bytes_read == 0)
        {
            printf("[Thread] Client socket %d closed connection.\n", client_fd);
            break;
        }
        else if (bytes_read == -1)
        {
            fprintf(stderr, "[Thread] recv error on socket %d: %s\n", client_fd, strerror(errno));
            break;
        }
        else
        {
            buffer[bytes_read] = '\0';
            printf("Message received from client %d: \"%s\"\n", client_fd, buffer);

            // Convertir a mayúsculas
            for (int i = 0; i < bytes_read; i++)
            {
                buffer[i] = toupper((unsigned char)buffer[i]);
            }

            sleep(1); // Simular procesamiento pesado como en Python

            int bytes_sent = send(client_fd, buffer, bytes_read, 0);
            if (bytes_sent == -1)
            {
                fprintf(stderr, "send error: %s\n", strerror(errno));
                break;
            }
        }
    }

    close(client_fd);
    printf("[Thread] Closed client socket %d\n", client_fd);
    return NULL;
}

int main(void)
{
    printf("---- MULTITHREADED SERVER ----\n\n");
    struct sockaddr_in sa;
    int socket_fd;
    int status;

    memset(&sa, 0, sizeof sa);
    sa.sin_family = AF_INET;
    sa.sin_addr.s_addr = htonl(INADDR_ANY); // Aceptar conexiones de cualquier IP
    sa.sin_port = htons(PORT);

    socket_fd = socket(sa.sin_family, SOCK_STREAM, 0);
    if (socket_fd == -1)
    {
        fprintf(stderr, "socket fd error: %s\n", strerror(errno));
        return (1);
    }

    // Configuración para reutilizar el puerto inmediatamente
    int opt = 1;
    setsockopt(socket_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));

    status = bind(socket_fd, (struct sockaddr *)&sa, sizeof sa);
    if (status != 0)
    {
        fprintf(stderr, "bind error: %s\n", strerror(errno));
        return (2);
    }

    printf("Listening on port %d\n", PORT);
    status = listen(socket_fd, BACKLOG);
    if (status != 0)
    {
        fprintf(stderr, "listen error: %s\n", strerror(errno));
        return (3);
    }

    while (1)
    {
        struct sockaddr_storage client_addr;
        socklen_t addr_size = sizeof client_addr;

        int *client_fd = malloc(sizeof(int)); // Asignar memoria para el descriptor
        *client_fd = accept(socket_fd, (struct sockaddr *)&client_addr, &addr_size);

        if (*client_fd == -1)
        {
            fprintf(stderr, "client fd error: %s\n", strerror(errno));
            free(client_fd);
            continue;
        }

        printf("Accepted new connection, spawning thread...\n");
        pthread_t thread_id;
        if (pthread_create(&thread_id, NULL, handle_client, client_fd) != 0)
        {
            fprintf(stderr, "Failed to create thread\n");
            free(client_fd);
        }

        pthread_detach(thread_id); // Liberar recursos del hilo al terminar
    }

    close(socket_fd);
    return (0);
}