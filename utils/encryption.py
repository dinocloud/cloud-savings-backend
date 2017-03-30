import boto3
import base64
KMS_KEY_ID = 'arn:aws:kms:sa-east-1:847874569360:key/732bbb1a-c88a-4e87-81a3-04d23ac8c9c1'


def encrypt(plain_text, context=None):
    client = boto3.client('kms')
    if context is not None:
        response = client.encrypt(KeyId=KMS_KEY_ID, Plaintext=plain_text,
                                  EncryptionContext=context)
    else:
        response = client.encrypt(KeyId=KMS_KEY_ID, Plaintext=plain_text)
    return base64.b64encode(response.get("CiphertextBlob"))


def decrypt(cipher_text_blob, context=None):
    client = boto3.client('kms')
    cipher_text_blob = base64.b64decode(cipher_text_blob)
    if context is not None:
        response = client.decrypt(CiphertextBlob=cipher_text_blob, EncryptionContext=context)
    else:
        response = client.decrypt(CiphertextBlob=cipher_text_blob)
    return response.get("Plaintext")

