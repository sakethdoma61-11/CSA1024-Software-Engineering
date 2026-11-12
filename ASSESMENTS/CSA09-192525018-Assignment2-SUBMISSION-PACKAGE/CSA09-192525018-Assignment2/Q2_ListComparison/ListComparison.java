import java.util.*;

public class ListComparison {
    private static long timeNanos(Runnable action) {
        long start = System.nanoTime();
        action.run();
        return System.nanoTime() - start;
    }

    private static void runSize(int n) {
        List<Integer> array = new ArrayList<>();
        List<Integer> linked = new LinkedList<>();
        for (int i = 0; i < n; i++) { array.add(i); linked.add(i); }

        int repetitions = Math.max(100, 100000 / Math.max(1, n));
        long arrayGet = timeNanos(() -> { long sum = 0; for (int r=0;r<repetitions;r++) sum += array.get(n/2); });
        long linkedGet = timeNanos(() -> { long sum = 0; for (int r=0;r<repetitions;r++) sum += linked.get(n/2); });

        long arrayFront = timeNanos(() -> { for (int r=0;r<repetitions;r++) { array.add(0, -r); array.remove(0); } });
        long linkedFront = timeNanos(() -> { for (int r=0;r<repetitions;r++) { linked.add(0, -r); linked.remove(0); } });

        long arrayIter = timeNanos(() -> { long sum=0; for (int x:array) sum+=x; });
        long linkedIter = timeNanos(() -> { long sum=0; for (int x:linked) sum+=x; });

        System.out.printf("n=%d | get(mid) ns: ArrayList=%d LinkedList=%d | front add/remove ns: ArrayList=%d LinkedList=%d | iteration ns: ArrayList=%d LinkedList=%d%n",
                n, arrayGet, linkedGet, arrayFront, linkedFront, arrayIter, linkedIter);

        Deque<Integer> upNext = new ArrayDeque<>();
        upNext.addFirst(1); upNext.addLast(2); upNext.removeFirst();
        System.out.println("ArrayDeque Up Next sample: " + upNext);
    }

    public static void main(String[] args) {
        runSize(1000);
        runSize(10000);
        runSize(50000);
    }
}
