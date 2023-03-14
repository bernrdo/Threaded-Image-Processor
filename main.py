import cv2
import threading
import time


def apply_filter(img, filter_type, start_row, end_row):
    """
    Aplica um filtro em uma parte da imagem.

    img: imagem a ser processada.
    filter_type: tipo de filtro a ser aplicado.
    start_row: linha de início da região a ser processada.
    end_row: linha final da região a ser processada.
    """
    for row in range(start_row, end_row):
        for col in range(img.shape[1]):
            if filter_type == 'grayscale':
                gray_value = int(0.3 * img[row][col][0] + 0.59 * img[row][col][1] + 0.11 * img[row][col][2])
                img[row][col] = [gray_value, gray_value, gray_value]
            elif filter_type == 'negative':
                img[row][col] = 255 - img[row][col]


def process_image_with_threads(img_path, filter_type, num_threads):
    """
    Carrega a imagem e processa com o filtro especificado utilizando threads.

    img_path: caminho da imagem a ser processada.
    filter_type: tipo de filtro a ser aplicado.
    num_threads: número de threads a serem utilizadas.
    """
    img = cv2.imread(img_path)
    if img is None:
        print('Erro ao carregar a imagem')
        return

    start_time = time.time()

    threads = []
    rows_per_thread = img.shape[0] // num_threads
    start_row = 0
    end_row = rows_per_thread

    for i in range(num_threads):
        t = threading.Thread(target=apply_filter, args=(img, filter_type, start_row, end_row))
        threads.append(t)
        start_row = end_row
        end_row = start_row + rows_per_thread

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    end_time = time.time()

    print(f'Tempo total de processamento: {end_time - start_time:.4f} segundos')
    print(f'Tempo de processamento por thread: {(end_time - start_time) / num_threads:.4f} segundos')

    cv2.imshow('Imagem Processada', img)
    cv2.waitKey(0)


if __name__ == '__main__':
    img_path = input('Digite o caminho da imagem: ')
    filter_type = input('Digite o tipo de filtro a ser aplicado (grayscale ou negative): ')
    num_threads = int(input('Digite o número de threads a serem utilizadas: '))

    process_image_with_threads(img_path, filter_type, num_threads)
