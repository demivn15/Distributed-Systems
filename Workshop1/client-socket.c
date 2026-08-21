// Client socket in C (Multithreaded & Automated)
#include <errno.h>
#include <netdb.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <unistd.h>
#include <pthread.h>
#include <time.h>
#include <arpa/inet.h>
#include <netinet/in.h> // Asegura la correcta traducción de puertos

#define PORT 12000
#define NUM_CLIENTS 3

char server_ip[64];

typedef struct
{
    int client_id;
} thread_data_t;

void *client_thread(void *arg)
{
    thread_data_t *data = (thread_data_t *)arg;
    int client_id = data->client_id;
    free(data);

    struct sockaddr_in sa;
    int socket_fd;
    char buffer[BUFSIZ];

    memset(&sa, 0, sizeof sa);
    sa.sin_family = AF_INET; // IPv4
    sa.sin_port = htons(PORT);

    // NUEVO: Validación estricta y segura de la IP
    if (inet_pton(AF_INET, server_ip, &sa.sin_addr) <= 0)
    {
        fprintf(stderr, "[Client %d] Invalid IP address format: %s\n", client_id, server_ip);
        pthread_exit(NULL);
    }

    // Create socket, connect it to remote server[cite: 6]
    socket_fd = socket(sa.sin_family, SOCK_STREAM, 0);
    if (socket_fd == -1)
    {
        fprintf(stderr, "[Client %d] socket fd error: %s\n", client_id, strerror(errno));
        pthread_exit(NULL);
    }

    if (connect(socket_fd, (struct sockaddr *)&sa, sizeof sa) != 0)
    {
        fprintf(stderr, "[Client %d] connect error: %s\n", client_id, strerror(errno));
        close(socket_fd);
        pthread_exit(NULL);
    }

    printf("[Client %d] Connected to server %s:%d\n", client_id, server_ip, PORT);

    int num_messages = (rand() % 3) + 1;
    for (int i = 0; i < num_messages; i++)
    {
        char random_text[9];
        for (int j = 0; j < 8; j++)
        {
            random_text[j] = 'a' + (rand() % 26);
        }
        random_text[8] = '\0';

        char msg[256];
        sprintf(msg, "client %d msg %d: %s", client_id, i + 1, random_text);
        int msg_len = strlen(msg);

        // Send a message to server[cite: 6]
        if (send(socket_fd, msg, msg_len, 0) == -1)
        {
            fprintf(stderr, "[Client %d] send error\n", client_id);
            break;
        }

        // Wait for message from server via the socket[cite: 6]
        int bytes_read = recv(socket_fd, buffer, BUFSIZ - 1, 0);
        if (bytes_read > 0)
        {
            buffer[bytes_read] = '\0';
            printf("[Client %d] Response from server: \"%s\"\n", client_id, buffer);
        }
    }

    close(socket_fd);
    printf("[Client %d] Finished and closed socket\n", client_id);
    return NULL;
}

int main(void)
{
    printf("---- AUTOMATED MULTITHREADED CLIENT ----\n\n");
    srand(time(NULL));

    printf("Enter server IP address (e.g., 127.0.0.1): ");

    // NUEVO: Limpiamos cualquier salto de línea o espacio basura que Cygwin pueda meter
    if (fgets(server_ip, sizeof(server_ip), stdin) != NULL)
    {
        server_ip[strcspn(server_ip, "\r\n ")] = '\0';
    }

    pthread_t threads[NUM_CLIENTS];

    for (int i = 0; i < NUM_CLIENTS; i++)
    {
        thread_data_t *data = malloc(sizeof(thread_data_t));
        data->client_id = i + 1;

        if (pthread_create(&threads[i], NULL, client_thread, data) != 0)
        {
            fprintf(stderr, "Failed to create thread %d\n", i + 1);
        }
    }

    for (int i = 0; i < NUM_CLIENTS; i++)
    {
        pthread_join(threads[i], NULL);
    }

    printf("All clients finished.\n");
    return 0;
}
