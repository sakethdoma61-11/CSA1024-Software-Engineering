import java.io.*;
import java.nio.file.*;
public class ResourceDemo {
 static void writeReport(Path out,Path... inputs)throws IOException {
  try(BufferedWriter w=Files.newBufferedWriter(out)) {
   for(Path p:inputs){ try(BufferedReader r=Files.newBufferedReader(p)){ String line; while((line=r.readLine())!=null) w.write(line+"\\n"); } }
  }
 }
 public static void main(String[] args)throws Exception {
  Path dir=Files.createTempDirectory("sales-demo"); Path a=dir.resolve("store1.txt"),b=dir.resolve("store2.txt"),out=dir.resolve("summary.txt");
  Files.writeString(a,"Store 1: 1200"); Files.writeString(b,"Store 2: 850");
  writeReport(out,a,b); System.out.println(Files.readString(out).replace("\\n"," | "));
  try { writeReport(out,a,dir.resolve("missing.txt")); } catch(IOException e){System.out.println("Handled input failure: "+e.getClass().getSimpleName());}
  System.out.println("Try-with-resources closes opened files on success and failure.");
 }
}
