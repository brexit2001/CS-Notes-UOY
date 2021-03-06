# Semidecidable Languages

<br>

```ad-abstract
title: Theorem 4
collapse: closed
*A language L is semidecidable if and only if L is generated by some (unrestricted) grammar (so a Turing Machine will accept L)*
```

^f34ccb

| Type  | Grammars/ Languages              | Grammar productions                                                                                                         | Machines                                                          |
|:----- |:-------------------------------- |:--------------------------------------------------------------------------------------------------------------------------- |:----------------------------------------------------------------- |
| **0** | ***Unrestricted semidecidable*** | $\alpha \to \beta$<br>$[\alpha \in(\mathrm{V} \cup \Sigma)^{+},$<br>$\beta \in (\mathrm{V}\cup \Sigma)^{*}]$                | ***Turing machine* <br>(deterministic or <br> nondeterministic)** |
| 1     | *Context-sensitive*              | $\alpha \to \beta$<br>$[\alpha , \beta \in(\mathrm{V} \cup \Sigma)^{+},$<br>$\mid \alpha \mid \ \leq \ \mid \beta \mid \ ]$ | *Linear-bounded automaton*                                        |
| 2     | *Context-free*                   | $\mathrm{A} \to \beta$<br>$[\mathrm{A}\in \mathrm{V},\ \beta \in (V\cup\Sigma)^{*}]$                                        | *Pushdown automaton*                                              |
| 3     | *Regular*                        | $\mathrm{A} \to \mathrm{aB},\ \mathrm{A}\to \lambda$<br>$[\mathrm{A,\ B \in \ V, \ a \in \Sigma}]$                          | *Finite automaton* <br>(deterministic or <br> nondeterministic)   |

---

# Enumeration

A [[Lecture 5 Variations on Turing Machines#Multitape Turing Machines|Multitape Turing Machine]] will enumerate a language if:

1) At the start all tapes are blank
2) Tape 1 never moves to the left
3) At every step of the computation, a string of symbols from the language will be added to tape 1. Every slot between characters will have a divider symbol
4) Eventually, we'll have every symbol from the language on tape 1

```ad-warning
There can be repeated strings
```

*Example*:

This is for the language $\mathrm{L} = \{\mathrm{a^n \ b^n \ c^n \ \mid n\geq 0}\}$

![[Enumeration.png|600]]

For the string $\#\# a b c\#$
$$\begin{aligned}\left(q_{0} \Delta, q_{0} \Delta\right) & \vdash\left(\Delta q_{1} \Delta, \Delta q_{1} \Delta\right) \\ & \vdash\left(\Delta \# q_{2} \Delta, \Delta q_{2} a\right) \\ & \vdash\left(\Delta \# \# q_{3} \Delta, \Delta q_{3} a\right) \\ & \vdash\left(\Delta \# \# a q_{3} \Delta, \Delta a q_{3} \Delta\right) \\ & \vdash\left(\Delta \# \# a q_{4} \Delta, \Delta q_{4} a \Delta\right) \\ & \vdash\left(\Delta \# \# a b q_{4} \Delta, q_{4} \Delta a \Delta\right) \\ & \vdash\left(\Delta \# \# a b q_{5} \Delta, \Delta q_{5} a \Delta\right) \\ & \vdash\left(\Delta \# \# a b c q_{5} \Delta, \Delta a q_{5} \Delta\right) \\ & \vdash\left(\Delta \# \# a b c q_{6} \Delta, \Delta q_{6} a a\right) \\ & \vdash\left(\Delta \# \# a b c q_{6} \Delta, q_{6} \Delta a a\right) \\ & \vdash\left(\Delta \# \# a b c \# q_{3} \Delta, \Delta q_{3} a a\right) \end{aligned}$$

```ad-abstract
title: Theorem 5
collapse: closed
*A language L is enumerated by some multitape Turing machine if and only if L is semidecidable.*
```

^e48461
