| Operation | ArrayList | LinkedList | ArrayDeque |
|---|---:|---:|---:|
| Add at end | O(1) amortized | O(1) | O(1) amortized |
| Add/remove at front | O(n) | O(1) | O(1) amortized |
| Insert in middle by index | O(n) | O(n) to locate, O(1) link change | Not index-oriented |
| Get k-th element | O(1) | O(n) | O(n) if traversed |
| Full iteration | O(n) | O(n) | O(n) |

ArrayDeque is a strong fit for the changed Up Next requirement (add at both ends and remove from front). The benchmark is a simple local experiment; repeat runs and report the actual environment and averages.
