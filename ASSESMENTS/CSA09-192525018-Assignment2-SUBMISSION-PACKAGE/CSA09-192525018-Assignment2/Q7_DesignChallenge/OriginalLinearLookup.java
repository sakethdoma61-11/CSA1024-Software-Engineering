import java.util.ArrayList;
import java.util.List;

public class OriginalLinearLookup {
    private final List<String> codes = new ArrayList<>();

    public void add(String code) { codes.add(code); }

    public int find(String code) {
        for (int i = 0; i < codes.size(); i++) {
            if (codes.get(i).equals(code)) return i;
        }
        return -1;
    }

    public static void main(String[] args) {
        OriginalLinearLookup inventory = new OriginalLinearLookup();
        for (int i = 0; i < 100000; i++) inventory.add(String.format("ITEM%06d", i));
        long start = System.nanoTime();
        int result = inventory.find("ITEM099999");
        System.out.println("Index=" + result + ", elapsed ns=" + (System.nanoTime() - start));
    }
}
