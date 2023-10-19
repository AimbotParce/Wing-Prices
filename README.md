# Wing-Prices

Somebody posted the following on reddit:

![Wings Menu](https://github.com/AimbotParce/Wing-Prices/blob/main/about/Wings_menu.jpg?raw=true)

With the caption "Surely, there's gotta be a better way of conveying this information", which unveiled dozens of comments from people who, like me, can only be described as psychopaths. That's because it's not the way the information that drove us crazy, but the fact that the prices do not follow any pattern!

As someone on the internet pointed out, the price per wing graph for this menu, depending on the wing total makes for an amazing minimization problem to get the best price for N wings.

![Price per wing](https://github.com/AimbotParce/Wing-Prices/blob/main/about/Price_per_wing.png?raw=true)

Some have even tried to come up with a strategy to calculate the price of buying N wings for any N:

$$
n \text{ wings} \approx \frac{1}{20} \left\lfloor 20 \times \frac{\$17 n}{15}\right\rfloor
$$

But as the person who came up with it poited out, this formula breaks down at 24 wings.

Now this itself is already very interesting, but for those of us who love chicken wings, there's not enough with knowing the price, but we want to get the best deal. So, with the help of my excel skills (this is what my physics degree has ended up in), it was easy to find what the best deal for N wings is: The cheapest overall cost per wing is $1.112, which can be obtained by buying 25, 50 or 125 wings; and the most expensive overall cost per wing is $1.14, for 5 wings. This is consistent with what people have been pointing up in some comments.

But here's my concern: What happens if I want to buy 34 wings? Or 57? Or 169? How much am I paying there? Some might say "Well, 34 wings is a 30 pack plus a 4 pack, for a total of $38.05" and to that I say: You fools, If you would have bought a 25 pack and a 9 pack, you would have saved $0.05!

So, finally, here's what all of this is about: Let's say I want to save as much money as possible, but still buy N chicken wings. What's the absolute minimum I can pay, and how do I get there? **Don't worry, I've got you covered.** [Here's my study](#The-Study) on the matter, with [the table of the best combinations to get N wings from 1 to 500](#Results).


Here's the table with all the data used for this analysis:
| Chicken   Wing Count (w) | Price ($) | Wing Increment (Δw) | Price Increment   (Δ$) | New Wings Price   (Δ$/Δw) | Price per wing   ($/w) |
|--------------------------|-----------|---------------------|------------------------|---------------------------|------------------------|
| 4                        | $4.55     | 4                   | $4.55                  | $1.1375                   | $1.1375                |
| 5                        | $5.70     | 1                   | $1.15                  | $1.1500                   | $1.1400                |
| 6                        | $6.80     | 1                   | $1.10                  | $1.1000                   | $1.1333                |
| 7                        | $7.95     | 1                   | $1.15                  | $1.1500                   | $1.1357                |
| 8                        | $9.10     | 1                   | $1.15                  | $1.1500                   | $1.1375                |
| 9                        | $10.20    | 1                   | $1.10                  | $1.1000                   | $1.1333                |
| 10                       | $11.35    | 1                   | $1.15                  | $1.1500                   | $1.1350                |
| 11                       | $12.50    | 1                   | $1.15                  | $1.1500                   | $1.1364                |
| 12                       | $13.60    | 1                   | $1.10                  | $1.1000                   | $1.1333                |
| 13                       | $14.75    | 1                   | $1.15                  | $1.1500                   | $1.1346                |
| 14                       | $15.90    | 1                   | $1.15                  | $1.1500                   | $1.1357                |
| 15                       | $17.00    | 1                   | $1.10                  | $1.1000                   | $1.1333                |
| 16                       | $18.15    | 1                   | $1.15                  | $1.1500                   | $1.1344                |
| 17                       | $19.30    | 1                   | $1.15                  | $1.1500                   | $1.1353                |
| 18                       | $20.40    | 1                   | $1.10                  | $1.1000                   | $1.1333                |
| 19                       | $21.55    | 1                   | $1.15                  | $1.1500                   | $1.1342                |
| 20                       | $22.70    | 1                   | $1.15                  | $1.1500                   | $1.1350                |
| 21                       | $23.80    | 1                   | $1.10                  | $1.1000                   | $1.1333                |
| 22                       | $24.95    | 1                   | $1.15                  | $1.1500                   | $1.1341                |
| 23                       | $26.10    | 1                   | $1.15                  | $1.1500                   | $1.1348                |
| 24                       | $27.25    | 1                   | $1.15                  | $1.1500                   | $1.1354                |
| 25                       | $27.80    | 1                   | $0.55                  | $0.5500                   | $1.1120                |
| 26                       | $28.95    | 1                   | $1.15                  | $1.1500                   | $1.1135                |
| 27                       | $30.10    | 1                   | $1.15                  | $1.1500                   | $1.1148                |
| 28                       | $31.20    | 1                   | $1.10                  | $1.1000                   | $1.1143                |
| 29                       | $32.35    | 1                   | $1.15                  | $1.1500                   | $1.1155                |
| 30                       | $33.50    | 1                   | $1.15                  | $1.1500                   | $1.1167                |
| 35                       | $39.15    | 5                   | $5.65                  | $1.1300                   | $1.1186                |
| 40                       | $44.80    | 5                   | $5.65                  | $1.1300                   | $1.1200                |
| 45                       | $50.50    | 5                   | $5.70                  | $1.1400                   | $1.1222                |
| 50                       | $55.60    | 5                   | $5.10                  | $1.0200                   | $1.1120                |
| 60                       | $67.00    | 10                  | $11.40                 | $1.1400                   | $1.1167                |
| 70                       | $78.30    | 10                  | $11.30                 | $1.1300                   | $1.1186                |
| 75                       | $83.45    | 5                   | $5.15                  | $1.0300                   | $1.1127                |
| 80                       | $89.10    | 5                   | $5.65                  | $1.1300                   | $1.1138                |
| 90                       | $100.45   | 10                  | $11.35                 | $1.1350                   | $1.1161                |
| 100                      | $111.25   | 10                  | $10.80                 | $1.0800                   | $1.1125                |
| 125                      | $139.00   | 25                  | $27.75                 | $1.1100                   | $1.1120                |
| 150                      | $166.85   | 25                  | $27.85                 | $1.1140                   | $1.1123                |
| 200                      | $222.50   | 50                  | $55.65                 | $1.1130                   | $1.1125                |


## The Study

"The algorithm explained"

## Results

"the table"
