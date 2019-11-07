using System;
using System.Collections.Generic;
using System.Numerics;
using System.Text;

namespace ElGamal
{
    class ElGamal
    {

        public decimal P;

        public decimal g;

        public decimal KOpen;

        private decimal KClose;

        public ElGamal()
        {
            KeyGen();
        }

        public ElGamal(ulong p)
        {
            P = p; 
            KeyGen(P);
        }

        protected void KeyGen()
        {
            P = CreateBigPrime(10);
            g = TakePrimitiveRoot(P);
            KClose = 2;
            while (GCD(KClose, P) != 1)
            {
                KClose = CreateBigPrime(10) % (P - 1);
            }
            KOpen = PowMod(g, KClose, P);
        }

        protected void KeyGen(decimal prime)
        {
            g = TakePrimitiveRoot(prime);
            Random rand = new Random();
            KClose = 2;
            while (GCD(KClose, prime) != 1)
            {
                KClose = (rand.Next(1, Int32.MaxValue) * rand.Next(1, Int32.MaxValue)) % (prime - 1);
            }
            KOpen = PowMod(g, KClose, prime);
        }

        public static decimal GCD(decimal a, decimal b)
        {
            if (b == 0)
                return a;
            else
                return GCD(b, a % b);
        }

        protected decimal TakePrimitiveRoot(decimal primeNum)
        {
            for (ulong i = 0; i < primeNum; i++)
                if (IsPrimitiveRoot(primeNum, i))
                    return i;
            return 0;
        }

        public bool IsPrimitiveRoot(decimal p, decimal a)
        {
            if (a == 0 || a == 1)
                return false;
            decimal last = 1;
            HashSet<decimal> set = new HashSet<decimal>();
            for (ulong i = 0; i < p - 1; i++)
            {
                last = (last * a) % p;
                if (set.Contains(last)) 
                    return false;
                set.Add(last);
            }
            return true;
        }

        public List<decimal[]> Encrypting(string message)
        {
            byte[] binary = Encoding.UTF8.GetBytes(message);
            List<decimal[]> ciphermessage = new List<decimal[]>(); 
            Random rand = new Random();
            decimal[] pair = new decimal[2];
            decimal k = 0;
            for (int i = 0; i < binary.Length; i++)
            {
                k = (rand.Next(1, Int16.MaxValue) * rand.Next(1, Int16.MaxValue)) % (P - 1);
                pair = new decimal[2];
                pair[0] = PowMod(g, k, P);
                pair[1] = (PowMod(KOpen, k, P) * binary[i]) % P;
                ciphermessage.Add(pair);
            }
            return ciphermessage;
        }

        public string Decrypting(List<decimal[]> ciphermesage)
        {
            string plain = "";
            byte n;
            for (int i = 0; i < ciphermesage.Count; i++)
            {
                n = (byte)((PowMod((decimal)EuclideanAlgorithm(P, ciphermesage[i][0]), KClose, P) * ciphermesage[i][1]) % P);
                plain += Encoding.ASCII.GetChars(new byte[] { n })[0];
            }
            return plain;
        }

        public static string GetPlainFromCipher(List<decimal[]> ciphermesage, decimal p, decimal g, decimal OpenKey)
        {
            string plain = "";
            byte n;
            decimal k;
            for (int i = 0; i < ciphermesage.Count; i++)
            {
                k = ElGamal.MatchingAlgorithm(g, ciphermesage[i][0], p);
                n = (byte)((ElGamal.PowMod(ElGamal.EuclideanAlgorithm(p, OpenKey), k, p) * ciphermesage[i][1]) % p);
                Console.WriteLine($"{ciphermesage[i][0]} = {g}^k mod {p}\nk = {k}");
                Console.WriteLine($"M = {n} = (({OpenKey})^-1)^{k} * {ciphermesage[i][1]} mod {p}");
                plain += Encoding.ASCII.GetChars(new byte[] { n })[0];
            }
            return plain;
        }

        public static decimal EuclideanAlgorithm(decimal module, decimal element)
        {
            decimal inverse = 0;
            decimal w1 = 0, w3 = module, r1 = 1, r3 = element; 
            decimal q = (decimal)Math.Floor((w3 / r3));
            decimal cr1, cr3;
            while (r3 != 1)
            {
                cr1 = r1;
                cr3 = r3;
                r1 = w1 - r1 * q;
                r3 = w3 - r3 * q;
                w1 = cr1;
                w3 = cr3;
                q = Math.Floor(w3 / r3);
            }

            inverse = r1;
            if (inverse < 0) 
            {
                inverse += module;
            }

            return inverse;
        }

        public static decimal MatchingAlgorithm(decimal a, decimal b, decimal p)
        {
            decimal x = 0,
                H = (long)Math.Sqrt(Decimal.ToUInt64(p)) + 1;
            decimal c = PowMod(a, H, p);
            List<decimal> table_0 = new List<decimal>(),
                table_1 = new List<decimal>();
            table_1.Add((b % p));
            for (long i = 1; i <= H; i++)
            {
                table_0.Add(PowMod(c, i, p));
                table_1.Add(((PowMod(a, i, p) * b) % p));
            }
            decimal q;
            for (short i = 0; i < table_1.Count; i++)
            {
                q = table_0.IndexOf(table_1[i]);
                if (q > 0)
                {
                    x = ((q + 1) * H - i);
                    break;
                }
            }
            return x;
        }

        public ulong CreateBigPrime(short numDec)
        {
            ulong N = 1;
            Random rand = new Random(DateTime.Now.Millisecond);
            while (Convert.ToString(N).Length < numDec || !isPrime(N))
            {
                N = (ulong)(rand.Next(0, int.MaxValue) * rand.Next(0, int.MaxValue)) - 1;
            }
            return N;
        }

        public bool isPrime(ulong n)
        {
            for (ulong i = 2; i < n / 2 + 1; i++)
            {
                if ((n % i) == 0) return false;
            }
            return true;
        }

        public static decimal PowMod(decimal number, decimal pow, decimal module)
        {
            string q = Convert.ToString((long)pow, 2); 
            BigInteger s = 1, c = (BigInteger)number; 
            for (int i = q.Length - 1; i >= 0; i--)
            {
                if (q[i] == '1')
                {
                    s = (s * c) % (BigInteger)module;
                }
                c = (c * c) % (BigInteger)module;
            }
            return (decimal)s;
        }
    }
}
