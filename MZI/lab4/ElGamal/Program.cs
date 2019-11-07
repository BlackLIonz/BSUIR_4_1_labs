using System;
using System.Collections.Generic;

namespace ElGamal
{
    class Program
    {
        static void Main(string[] args)
        {
            ElGamal q = new ElGamal(20996023);
            Console.WriteLine($"P: {q.P}\ng: {q.g}\nOpen: {q.KOpen}");
            string message = "Test ElGamal";
            Console.WriteLine("Input text: " + message);
            List<decimal[]> text = q.Encrypting(message);

            Console.WriteLine("Encrypted:");
            Console.WriteLine(String.Join(" ", text));
     
            Console.WriteLine("Decrypted..." + ElGamal.GetPlainFromCipher(text, q.P, q.g, q.KOpen));

            Console.WriteLine("Decrypted:");
            Console.WriteLine(q.Decrypting(text));

            Console.ReadKey();
        }
    }
}
