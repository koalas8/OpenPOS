using System;
using System.Collections.Generic;
using System.Collections;
using System.Linq;
using System.Text;
using System.Security;
using System.Security.Cryptography;

namespace CardGenerator
{
    public class Utils
    {
        /// <summary>
        /// 在给定的字符前补0
        /// </summary>
        /// <param name="str">给定的字符</param>
        /// <param name="length">补0后的长度</param>
        /// <returns></returns>
        public static String zfill(String str, int length)
        {
            while (str.Length < length)
            {
                str = "0" + str;
            }
            return str;
        }

        /// <summary>
        /// 生成长度为length的随机数字字符串
        /// </summary>
        /// <param name="length">要返回的随机字符串的长度</param>
        /// <returns></returns>
        public static String random(int length)
        {
            ArrayList arrayList = new ArrayList();
            String str = "0,1,2,3,4,5,6,7,8,9";
            arrayList.AddRange(str.Split(','));

            //随机码
            String randomContent = "";
            String seed = "";
            String guid = System.Guid.NewGuid().ToString("N").Replace('a', '1').Replace('b','2').Replace('c','3').Replace('d','4').Replace('e','5').Replace('f','6');
            Random rd = new Random(Convert.ToInt32(guid.Substring(26)));

            for (int i = 0; i < length; i++)
            {
                randomContent += arrayList[rd.Next(0, 9)];
            }
            return randomContent;
        }

        /// <summary>
        /// MD5加密字符串
        /// </summary>
        /// <param name="strToEncrypt"></param>
        /// <returns></returns>
        public static String md5(String strToEncrypt)
        {
            MD5 md5 = new MD5CryptoServiceProvider();
            byte[] result = md5.ComputeHash(System.Text.Encoding.Default.GetBytes(strToEncrypt));
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
