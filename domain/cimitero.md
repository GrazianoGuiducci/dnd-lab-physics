# Cimitero — Claim falsificati o declassati

> Qui finisce cio' che non ha superato il dubbio.
> Ogni voce: cosa diceva, perche' e' uscita, cosa l'ha sostituita, data.
> Il cimitero e' la memoria del filtro. Senza cimitero, il condensato non sa calibrarsi.

---

### lambda_2 converges to -0.558, NOT to -1/phi = -0.618. Measured with std = 0.0000

**Cosa diceva**: lambda_2 converges to -0.558, NOT to -1/phi = -0.618. Measured with std = 0.000041 across multiples of 3 for m >= 15.

**Come è caduto**: Lens L3 (counter-pole). The prior report (agent_20260501_1256) computed the mod-6 transition matrix with 788,056 gaps (primes to 12M) and found eigenvalues 1.000, -0.551, -0.042. This report uses only 148,929 gaps (primes to 2M) and finds eigenvalues 1.000, -0.048, -0.557 at mod 6. With 5× more data the earlier experiment got lambda_2 = -0.551, which is FURTHER from -0.558 than the smaller-sample result -0.557. If the true asymptotic were -0.558, more data should push closer to it, not away. The transition probabilities also differ: P(2→4) = 0.5508 (12M) vs 0.5573 (2M). The report never checks N-convergence of lambda_2 itself — only convergence across moduli at a single N.

**Sostituito da**: Run the spectral scan at multiple N (e.g., 500K, 1M, 2M, 5M, 12M primes) for at least mod 3 and mod 6. Plot lambda_2(N). The previous report's -0.551 at 12M vs this report's -0.557 at 2M suggests the true asymptotic may be closer to -0.55, not -0.558. The claimed 4th-decimal precision (std=0.000041) is across-moduli variance, not across-N convergence — these are different things.

**Data falsificazione**: cycle 20260501_1514, falsifier_20260501_1514.json (decisione CRYSTALLIZE high del valutatore)

---

### This is a universal constant of the prime gap sequence, visible from any modulus

**Cosa diceva**: This is a universal constant of the prime gap sequence, visible from any modulus m >= 3.

**Come è caduto**: Lens L5 (counter-pole). The transition matrix biases in consecutive prime gaps mod q are the subject of Lemke Oliver & Soundararajan (2016), 'Unexpected biases in the distribution of consecutive primes.' Their work characterizes exactly these non-uniform transition probabilities (including the 2↔4 alternation at mod 6) and derives them from the Hardy-Littlewood prime k-tuples conjecture with a secondary term. The spectral properties of the transition matrix (including lambda_2) are a direct algebraic consequence of those biases. The report presents the spectral structure as a discovery without citing or acknowledging the closest classical result.

**Sostituito da**: Acknowledge Lemke Oliver–Soundararajan explicitly. Check whether their predicted transition probabilities (which are functions of N, converging slowly) yield a lambda_2 prediction that can be compared to the measured value. The 'universal constant' framing should be replaced with: 'lambda_2 is determined by the Lemke Oliver–Soundararajan bias structure — here we measure its spectral consequence.'

**Data falsificazione**: cycle 20260501_1514, falsifier_20260501_1514.json (decisione CRYSTALLIZE high del valutatore)

---

### Verdict: CONFIRMED + NEW — the Markov-1 chain explains at most 0.5% of the signi

**Cosa diceva**: Verdict: CONFIRMED + NEW — the Markov-1 chain explains at most 0.5% of the significant autocorrelation structure

**Come è caduto**: Lens L5 (counter-pole). A first-order Markov chain on k states has autocorrelation ACF(lag) = sum_i c_i * lambda_i^lag. For |lambda_2|=0.558, this decays to <0.001 by lag 5 (0.558^5=0.053). The Markov chain being unable to explain lag 20+ is a textbook consequence of geometric spectral decay, not a discovery. Likewise, long-range positive autocorrelation of prime gaps is a known consequence of the slow growth of 1/ln(p) (prime density modulation). The closest classical reference — Lemke Oliver & Soundararajan (2016) on short-range prime gap biases — is not cited, nor is the standard PNT-based explanation for long-range gap correlation acknowledged as prior art. Tagging this as NEW without these acknowledgements is beauty bias.

**Sostituito da**: Next cycle should: (1) compute the expected ACF from 1/ln(p) density variation alone and compare to the observed long-range ACF ~0.005-0.009; if they match, this is a re-derivation of PNT, not a new finding. (2) Explicitly cite Lemke Oliver-Soundararajan 2016 as the classical framework for short-range gap mod q biases. (3) Reframe: the contribution is the quantitative decomposition and the desert boundary, not the Markov insufficiency which is a mathematical tautology.

**Data falsificazione**: cycle 20260503_0806, falsifier_20260503_0806.json (decisione CRYSTALLIZE high del valutatore)

---

*Il cimitero cresce. Il condensato si densifica. Il rapporto tra i due e' la misura della maturita' del filtro.*
