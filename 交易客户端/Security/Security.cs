using System;
using System.Security.Cryptography;
using System.Collections.Generic;
using System.IO;
using System.Text;
using System.Collections;

namespace CoolCard
{
    public class Security
    {
        /// <summary>
        /// AES加密
        /// </summary>
        /// <param name="stringToEncrypt">明文</param>
        /// <returns>base64编码的密文</returns>
        public string AESEncript(String stringToEncrypt)
        {
            byte[] keyArray = UTF8Encoding.UTF8.GetBytes("12345678901234567890123456789012");
            byte[] toEncryptArray = UTF8Encoding.UTF8.GetBytes(stringToEncrypt);

            RijndaelManaged rDel = new RijndaelManaged();
            rDel.Key = keyArray;
            rDel.Mode = CipherMode.ECB;
            rDel.Padding = PaddingMode.ANSIX923;

            ICryptoTransform cTransform = rDel.CreateEncryptor();
            byte[] resultArray = cTransform.TransformFinalBlock(toEncryptArray, 0, stringToEncrypt.Length);
            return Convert.ToBase64String(resultArray);
        }


        /// <summary>
        /// AES解密
        /// </summary>
        /// <param name="stringToDecrypt">base64编码的密文</param>
        /// <returns>明文</returns>
        public string AESDecrypt(string stringToDecrypt)
        {
            stringToDecrypt = stringToDecrypt.Replace("\n", "");
            byte[] keyArray = UTF8Encoding.UTF8.GetBytes("12345678901234567890123456789012");
            byte[] toDecryptArray = Convert.FromBase64String(stringToDecrypt);

            RijndaelManaged rDel = new RijndaelManaged();
            rDel.Key = keyArray;
            rDel.Mode = CipherMode.ECB;
            rDel.Padding = PaddingMode.ANSIX923;

            ICryptoTransform cTransform = rDel.CreateDecryptor();
            byte[] resultArray = cTransform.TransformFinalBlock(toDecryptArray, 0, toDecryptArray.Length);

            return UTF8Encoding.UTF8.GetString(resultArray);
        }

        /// <summary>
        /// DES加密
        /// </summary>
        /// <param name="data">明文</param>
        /// <param name="des_key">密钥</param>
        /// <returns>base64编码的密文</returns>
        public string DESEncrypt(string data, string des_key)
        {
            DESCryptoServiceProvider des = new DESCryptoServiceProvider();

            byte[] inputByte = System.Text.ASCIIEncoding.UTF8.GetBytes(data);
            byte[] key = Encoding.ASCII.GetBytes(des_key);
            MemoryStream ms = new MemoryStream();
            des.Key = key;
            des.IV = key;
            des.Mode = CipherMode.ECB;
            des.Padding = PaddingMode.PKCS7;
            CryptoStream cs = new CryptoStream(ms, des.CreateEncryptor(key, key), CryptoStreamMode.Write);
            cs.Write(inputByte, 0, inputByte.Length);
            cs.FlushFinalBlock();
            StringBuilder ret = new StringBuilder();

            return Convert.ToBase64String(ms.ToArray());

        }


        /// <summary>
        /// DES解密        
        /// </summary>
        /// <param name="data">base64编码的密文</param>
        /// <param name="des_key">密钥</param>
        /// <returns>明文</returns>
        public string DESDecrypt(string data, string des_key)
        {
            DESCryptoServiceProvider des = new DESCryptoServiceProvider();

            byte[] inputByte = System.Text.ASCIIEncoding.UTF8.GetBytes(data);
            byte[] key = Encoding.ASCII.GetBytes(des_key);
            MemoryStream ms = new MemoryStream();
            des.Key = key;
            des.IV = key;
            des.Mode = CipherMode.ECB;
            des.Padding = PaddingMode.PKCS7;
            CryptoStream cs = new CryptoStream(ms, des.CreateDecryptor(key, key), CryptoStreamMode.Read);
            StreamReader sr = new StreamReader(cs);
            return sr.ReadLine();
        }

        /// <summary>
        /// MD5加密
        /// </summary>
        /// <param name="data">明文</param>
        /// <returns>加密后的密文</returns>
        public static String MD5Encrypt(String data)
        {
            MD5 md5 = new MD5CryptoServiceProvider();
            byte[] result = md5.ComputeHash(System.Text.Encoding.Default.GetBytes(data));
            md5.Clear();
            String str = "";
            for (int i = 0; i < result.Length; i++)
            {
                str += result[i].ToString("x").PadLeft(2, '0');
            }
            return str;
        }
    }
}
