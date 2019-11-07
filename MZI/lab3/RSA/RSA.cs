using System;
using BigInteger = Org.BouncyCastle.Math.BigInteger;

namespace RSA
{
    public class RSA
    {
        private BigInteger p;
        private BigInteger q;
        private BigInteger n;
        private BigInteger fn;
        private BigInteger e;
        private BigInteger d;
        public RSA(int bits)
        {
            p = Helper.GenerateBigIntegerPrimes(bits);
            q = Helper.GenerateBigIntegerPrimes(bits);
            Console.WriteLine("p generated " + p);
            Console.WriteLine("q generated " + q);
            n = p.Multiply(q);
            Console.WriteLine("n = " + n);
            BigInteger p1 = p.Subtract(new BigInteger("1"));
            BigInteger q1 = q.Subtract(new BigInteger("1"));
            fn = p1.Multiply(q1);
            Console.WriteLine("Функция Эйлера = " + fn);
            int[] er = new[] { 17, 257, 65537 };
            Random rand = new Random((int)System.DateTime.Now.Ticks);
            e = new BigInteger(er[rand.Next(0, er.Length)].ToString());
            Console.WriteLine("e = " + e);

            d = e.ModInverse(fn);
            Console.WriteLine("d = " + d);

            Console.WriteLine("Public Key: " + e + ", " + n);
            Console.WriteLine("Private Key: " + d + ", " + n);
        }

        public BigInteger Encrypt(BigInteger m)
        {
            return m.ModPow(e, n);
        }

        public BigInteger Decrypt(BigInteger c)
        {
            return c.ModPow(d, n);
        }

        public class Helper
        {
            static public Org.BouncyCastle.Math.BigInteger GenerateBigIntegerPrimes(int bits)
            {
                Org.BouncyCastle.Security.SecureRandom ran = new Org.BouncyCastle.Security.SecureRandom();
                Org.BouncyCastle.Math.BigInteger c = new Org.BouncyCastle.Math.BigInteger(bits, ran);

                for (; ; )
                {
                    if (c.IsProbablePrime(100) == true) break;
                    c = c.Subtract(new Org.BouncyCastle.Math.BigInteger("1"));
                }
                return (c);
            }
        }
    }
}
