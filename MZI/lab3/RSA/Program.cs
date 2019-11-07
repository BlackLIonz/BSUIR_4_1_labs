using System;
using BigInteger = Org.BouncyCastle.Math.BigInteger;

namespace RSA
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Enter bits key length: ");
            int bit_len = int.Parse(Console.ReadLine());
            RSA rsa = new RSA(bit_len);
            Console.WriteLine("Enter string:");

            char[] array = Console.ReadLine().ToCharArray();
            BigInteger[] enStr = new BigInteger[array.Length];

            for (int i = 0; i < array.Length; ++i)
            {
                enStr[i] = rsa.Encrypt(new BigInteger(Convert.ToString((int)array[i])));
            }

            Console.WriteLine("Encrypted string: ");
            for (int i = 0; i < array.Length; ++i)
            {
                Console.Write(enStr[i].ToString());
            }

            char[] decArray = new char[array.Length];

            Console.WriteLine(" ");
            for (int i = 0; i < array.Length; ++i)
            {
                String decStr = rsa.Decrypt(enStr[i]).ToString();
                Console.WriteLine(decStr);
                decArray[i] = (char)int.Parse(decStr);
            }

            Console.WriteLine("\nDecrypt string: ");
            for (int i = 0; i < decArray.Length; ++i)
            {
                Console.Write(decArray[i]);
            }

            Console.ReadKey();
        }
    }
}
