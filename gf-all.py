import argparse
import subprocess
import os
import concurrent.futures

def execPattern(pattern, file, output_dir):
    output_file = os.path.join(output_dir, f"{pattern}.txt")

    with open(output_file, "w") as out_file:
        cat_process = subprocess.Popen(['cat', file], stdout=subprocess.PIPE)
        gf_process = subprocess.Popen(['gf', pattern], stdin=cat_process.stdout, stdout=out_file)
        cat_process.stdout.close()
        gf_process.communicate()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Este programa utiliza multithreading para aplicar todos os patterns do GF à uma lista de URL's.")
    parser.add_argument('url_file', type=str, help="Arquivo com URLs")
    parser.add_argument('output_dir', type=str, help="Caminho para a saída")
    parser.add_argument('--max-workers', type=int, default=2, help="Número máximo de threads para usar (padrão: 2)")

    args = parser.parse_args()

    if not os.path.isfile(args.url_file):
        print(f"Erro: O arquivo {args.url_file} não existe.")
        exit(1)

    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    command = ['gf', '-list']
    list_gf = subprocess.run(command, capture_output=True, text=True, check=True)
    list_gf = list_gf.stdout.split()

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.max_workers) as executor:
        futures = [executor.submit(execPattern, pattern, args.url_file, args.output_dir) for pattern in list_gf]
        # Espera todas as threads terminarem
        concurrent.futures.wait(futures)

    print("Processamento completo.")
