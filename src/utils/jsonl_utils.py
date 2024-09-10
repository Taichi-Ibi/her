from typing import Any, List
import json

def load_jsonl_file(
    file_path: str, ignore_error: bool = True, default_value: Any = []
) -> List[Any]:
    """
    Safe loading a JSONL file
    :param file_path: the path of the JSONL file
    :param ignore_error:
        if True, return default_value if error occurs and the error will be logged in debug level
        if False, raise error if error occurs
    :param default_value: the value returned when errors ignored
    :return: a list of objects from the JSONL content
    """
    try:
        with open(file_path, encoding="utf-8") as jsonl_file:
            try:
                jsonl_content = [json.loads(line) for line in jsonl_file]
                return jsonl_content if jsonl_content else default_value
            except json.JSONDecodeError as e:
                raise ValueError(f"Failed to parse JSONL file {file_path}: {e}")
    except Exception as e:
        if ignore_error:
            return default_value
        else:
            raise e

def write_jsonl_file(
    file_path: str,
    data: List[Any],
    ignore_error: bool = False,
    append: bool = False
) -> bool:
    """
    Safely write a list of objects to a JSONL file
    :param file_path: the path of the JSONL file to write
    :param data: a list of objects to write to the file
    :param ignore_error:
        if True, return False if error occurs and the error will be logged in debug level
        if False, raise error if error occurs
    :param append: if True, append to the existing file; if False, overwrite the file
    :return: True if successful, False if an error occurred and was ignored
    """
    mode = 'a' if append else 'w'
    try:
        with open(file_path, mode, encoding="utf-8") as jsonl_file:
            for item in data:
                json.dump(item, jsonl_file, ensure_ascii=False)
                jsonl_file.write('\n')
        return True
    except Exception as e:
        if ignore_error:
            # ここでログを記録するのもいいでしょう
            return False
        else:
            raise e