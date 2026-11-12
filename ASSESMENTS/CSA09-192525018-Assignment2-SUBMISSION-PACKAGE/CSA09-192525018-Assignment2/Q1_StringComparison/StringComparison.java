import java.util.StringJoiner;

public class StringComparison {
    private static final int WARMUP = 3;
    private static final int RUNS = 7;

    private static String buildWithPlus(String[] fields) {
        String result = "";
        for (String field : fields) result += field;
        return result;
    }

    private static String buildWithBuilder(String[] fields) {
        StringBuilder result = new StringBuilder();
        for (String field : fields) result.append(field);
        return result.toString();
    }

    private static String buildWithBuffer(String[] fields) {
        StringBuffer result = new StringBuffer();
        for (String field : fields) result.append(field);
        return result.toString();
    }

    private static long timeNanos(java.util.function.Supplier<String> task, int repetitions) {
        long start = System.nanoTime();
        String sink = "";
        for (int i = 0; i < repetitions; i++) sink = task.get();
        long elapsed = System.nanoTime() - start;
        if (sink.hashCode() == Integer.MIN_VALUE) System.out.println(sink);
        return elapsed;
    }

    private static void benchmark(String label, String[] fields, int repetitions) {
        java.util.function.Supplier<String> plus = () -> buildWithPlus(fields);
        java.util.function.Supplier<String> builder = () -> buildWithBuilder(fields);
        java.util.function.Supplier<String> buffer = () -> buildWithBuffer(fields);

        for (int i = 0; i < WARMUP; i++) {
            timeNanos(plus, repetitions);
            timeNanos(builder, repetitions);
            timeNanos(buffer, repetitions);
        }

        long plusTotal = 0, builderTotal = 0, bufferTotal = 0;
        for (int i = 0; i < RUNS; i++) {
            plusTotal += timeNanos(plus, repetitions);
            builderTotal += timeNanos(builder, repetitions);
            bufferTotal += timeNanos(buffer, repetitions);
        }

        System.out.printf("%s | repetitions=%d | average ns/ticket: + %.1f, Builder %.1f, Buffer %.1f%n",
                label, repetitions,
                plusTotal / (double) RUNS / repetitions,
                builderTotal / (double) RUNS / repetitions,
                bufferTotal / (double) RUNS / repetitions);
    }

    public static void main(String[] args) {
        String[] shortTicket = {"PNR:12345 ", "Name:Asha ", "Coach:S1 ", "Fare:500"};
        String[] mediumTicket = new String[50];
        String[] longTicket = new String[200];
        for (int i = 0; i < mediumTicket.length; i++) mediumTicket[i] = "Field" + i + "=value ";
        for (int i = 0; i < longTicket.length; i++) longTicket[i] = "Detail" + i + "=longer-value ";

        benchmark("Short ticket", shortTicket, 1000);
        benchmark("50 fields", mediumTicket, 1000);
        benchmark("200 fields", longTicket, 500);

        StringJoiner joiner = new StringJoiner(" | ");
        for (String field : shortTicket) joiner.add(field);
        System.out.println("StringJoiner example: " + joiner);
    }
}
