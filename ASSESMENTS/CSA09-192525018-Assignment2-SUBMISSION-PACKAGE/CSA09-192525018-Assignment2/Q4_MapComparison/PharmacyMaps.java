import java.util.*;

public class PharmacyMaps {
    private static Map<String, Integer> makeMap(SupplierType type) {
        Map<String, Integer> map;
        switch (type) {
            case HASH: map = new HashMap<>(); break;
            case TREE: map = new TreeMap<>(); break;
            default: map = new LinkedHashMap<>();
        }
        for (int i = 0; i < 10000; i++) map.put(String.format("MED%05d", i), 10 + i);
        return map;
    }

    enum SupplierType { HASH, TREE, LINKED }

    private static void test(SupplierType type) {
        Map<String, Integer> stock = makeMap(type);
        String key = "MED05000";
        long start = System.nanoTime();
        long checksum = 0;
        for (int i = 0; i < 100000; i++) checksum += stock.get(key);
        long lookupTime = System.nanoTime() - start;

        start = System.nanoTime();
        List<String> reportKeys = new ArrayList<>(stock.keySet());
        long reportTime = System.nanoTime() - start;

        System.out.printf("%s: 100000 lookups=%d ns, key-list report=%d ns, first=%s, last=%s, checksum=%d%n",
                type, lookupTime, reportTime, reportKeys.get(0),
                reportKeys.get(reportKeys.size()-1), checksum);
    }

    public static void main(String[] args) {
        test(SupplierType.HASH);
        test(SupplierType.TREE);
        test(SupplierType.LINKED);
    }
}
