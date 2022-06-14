import os
import uuid
import pandas
from os.path import exists
from threading import Timer
from shutil import make_archive, rmtree


def covert_symbol(symbol: str) -> str:
    if symbol == '>':
        return '$gte'
    elif symbol == '<':
        return '$lte'


def create_df(data: list) -> pandas.DataFrame:
    df = pandas.json_normalize(data)
    names = [name.replace('value.', '') for name in list(df.columns.tolist())]
    df.columns = names
    print(df.head())
    df.drop('_id', axis=1, inplace=True)
    return df


def process_data(df_list: list, device_names: list, save_as_one: bool) -> dict:
    file_name = generate_file_name()
    print(f'[+] file name has been generated')
    df = pandas.concat(df_list)
    if save_as_one:
        print(f'[+] saving as a single file')
        save_file_as_one(df, file_name)
        print(f'[+] file saved')
    else:
        print(f'[+] saving as separate files')
        os.mkdir(f'./files/{file_name}/')
        for i in range(len(df_list)):
            df_list[i].to_csv(path_or_buf=f'./files/{file_name}/'
                                          f'{device_names[i][0:index_of_last_num(device_names[i])]}.csv')
        print(f'[+] files saved inside a folder')
        zip_folder(folder_name=file_name)
        print(f'[+] folder has been compressed')
    return {
        'path': file_name,
        'rows': df.shape[0],
        'columns': df.shape[1],
        'preview': df.head().to_dict()
    }


def save_file_as_one(file: pandas.DataFrame, name: str):
    if not file.empty:
        compression_opts = dict(method='zip',
                                archive_name='data.csv')
        file.to_csv(path_or_buf=f'./files/{name}.zip', compression=compression_opts)
        start_timer(name)


def file_exists(file_name: str) -> bool:
    return exists(f'./files/{file_name}.zip')


def generate_file_name() -> str:
    return str(uuid.uuid4())


def delete_file(file_name: str):
    if exists(f'./files/{file_name}.zip'):
        os.remove(f'./files/{file_name}.zip')
        print(f'[+] {file_name} has been deleted')


def start_timer(file_name: str):
    print(f'[+] {file_name} will be deleted in 1 minute')
    Timer(interval=60, function=delete_file, args=[file_name]).start()


def index_of_last_num(name: str):
    index = 0
    for i in range(len(name)):
        try:
            int(name[i])
            index = i
        except ValueError:
            pass
    return index + 1


def filter_device_names(device_names: list) -> list:
    return [{'device_name': device[:index_of_last_num(device)] if device.count('sen') == 0 and device.count('acc') == 0
            else f'{device[:index_of_last_num(device)]} (sensor)' if device.count('sen') > 0
            else f'{device[:index_of_last_num(device)]} (accelerometer)', 'col_name': device}
            for device in device_names if device.startswith('M') or device.startswith('S')]


def zip_folder(folder_name: str):
    make_archive(f'./files/{folder_name}', 'zip', f'./files/{folder_name}')
    rmtree(f'./files/{folder_name}')
    start_timer(file_name=folder_name)
