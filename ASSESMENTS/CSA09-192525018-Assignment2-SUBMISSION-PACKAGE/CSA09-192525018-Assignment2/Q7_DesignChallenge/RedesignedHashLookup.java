import java.util.HashMap;
import java.util.Map;

public class RedesignedHashLookup {
    private final Map<String, Integer> indexByCode = new HashMap<>();

    public void add(String code, int stock) { indexByCode.put(code, stock); }

    public Integer find(String code) { return indexByCode.get(code); }

    public static void main(String[] args) {
        RedesignedHashLookup inventory = new RedesignedHashLookup();
        for (int i = 0; i < 100000; i++) inventory.add(String.format("ITEM%06d", i), i);
        long start = System.nanoTime();
        Integer result = inventory.find("ITEM099999");
        System.out.println("Stock=" + result + ", elapsed ns=" + (System.nanoTime() - start));
    }
}
