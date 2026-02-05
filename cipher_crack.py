#!/usr/bin/env python3
import argparse
import base64
import binascii
from urllib.parse import unquote
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

console = Console()

# Functions that try to decode common encodings and ciphers

def caesar_decrypt(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            shift_base = 65 if char.isupper() else 97
            result += chr((ord(char) - shift_base - shift) % 26 + shift_base)
        else:
            result += char
    return result

def rot13_decrypt(text):
    return caesar_decrypt(text, 13)

def base64_decode(text):
    try:
        decoded = base64.b64decode(text).decode()
        return decoded
    except Exception:
        return None

def xor_decrypt(text, key):
    decoded = ""
    for i, char in enumerate(text):
        decoded += chr(ord(char) ^ ord(key[i % len(key)]))
    return decoded

def vigenere_decrypt(text, key):
    key = key.upper()
    result = ""
    key_index = 0
    for char in text:
        if char.isalpha():
            shift_base = 65 if char.isupper() else 97
            key_char = key[key_index % len(key)]
            key_shift = ord(key_char) - 65
            result += chr((ord(char) - shift_base - key_shift) % 26 + shift_base)
            key_index += 1
        else:
            result += char
    return result

def try_caesar(text):
    results = []
    for shift in range(1, 26):
        decrypted = caesar_decrypt(text, shift)
        results.append({"method": f"Caesar shift {shift}", "result": decrypted})
    return results

def try_rot13(text):
    decrypted = rot13_decrypt(text)
    return [{"method": "ROT13", "result": decrypted}]

def try_base64(text):
    decoded = base64_decode(text)
    if decoded:
        return [{"method": "Base64", "result": decoded}]
    return []

def try_url_decode(text):
    try:
        decoded = unquote(text)
        if decoded != text:
            return [{"method": "URL Decode", "result": decoded}]
    except Exception:
        pass
    return []

def try_vigenere(text):
    #Trying out some usual keys
    common_keys = ["KEY", "CRYPTO", "SECRET", "PASS", "WORLD"]
    results = []
    for key in common_keys:
        decrypted = vigenere_decrypt(text, key)
        results.append({"method": f"Vigenère (key: {key})", "result": decrypted})
    return results

def try_xor(text):
    # Running through keys people often pick
    common_keys = ["key", "123", "a", "XOR", "secret"]
    results = []
    for key in common_keys:
        try:
            decrypted = xor_decrypt(text, key)
            results.append({"method": f"XOR (key: {key})", "result": decrypted})
        except Exception:
            continue
    return results

def detect_cipher_type(text):
    #See if it’s a Base64 string
    if len(text) % 4 == 0 and all(c in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=" for c in text):
        try:
            base64.b64decode(text)
            return "Base64"
        except Exception:
            pass

    #See if it’s plain text we can read.
    if all(32 <= ord(c) <= 126 for c in text):
        # Could be a classic cipher like Caesar or Vigenère
        return "Text"

    #Might be XOR-style encoding
    if any(0 <= ord(c) < 32 for c in text):
        return "XOR-like"

    return "Unknown"

def try_all_methods(text):
    results = []
    results.extend(try_caesar(text))
    results.extend(try_rot13(text))
    results.extend(try_base64(text))
    results.extend(try_url_decode(text))
    results.extend(try_vigenere(text))
    results.extend(try_xor(text))
    return results

def print_results_table(results):
    table = Table(title="Posibles Textos Descifrados", show_header=True, header_style="bold cyan")
    table.add_column("Método", style="magenta")
    table.add_column("Texto Descifrado", style="green", overflow="fold")

    for r in results:
        table.add_row(r["method"], r["result"])

    console.print(table)

def main():
    parser = argparse.ArgumentParser(description="Suite de criptoanálisis: descifra texto automáticamente")
    parser.add_argument("text", help="Texto encriptado a descifrar")
    parser.add_argument("--method", choices=["caesar", "rot13", "base64", "url", "vigenere", "xor"], help="Método específico a usar (opcional)")
    args = parser.parse_args()

    text = args.text
    method = args.method

    if method == "caesar":
        results = try_caesar(text)
    elif method == "rot13":
        results = try_rot13(text)
    elif method == "base64":
        results = try_base64(text)
    elif method == "url":
        results = try_url_decode(text)
    elif method == "vigenere":
        results = try_vigenere(text)
    elif method == "xor":
        results = try_xor(text)
    else:
        # Give all methods a shott
        cipher_type = detect_cipher_type(text)
        console.print(f"[blue]🔍 Cipher? Hmm, looks like: {cipher_type}[/blue]")
        results = try_all_methods(text)
        
    if results:
        print_results_table(results)
    else:
        console.print("[yellow]⚠️ No luck decrypting this one… maybe next time[/yellow]")

if __name__ == "__main__":
    main()
