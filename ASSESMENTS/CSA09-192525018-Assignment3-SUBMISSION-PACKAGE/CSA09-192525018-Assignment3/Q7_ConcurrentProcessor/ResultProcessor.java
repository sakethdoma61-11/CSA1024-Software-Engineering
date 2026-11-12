import java.nio.file.*; import java.io.*; import java.util.*; import java.util.concurrent.*; import java.util.concurrent.atomic.*;
public class ResultProcessor {
 record Outcome(String file,boolean success,String detail){}
 static Outcome process(Path p){try{String s=Files.readString(p).trim(); if(s.isEmpty())throw new IOException("Empty score file"); int score=Integer.parseInt(s); if(score<0||score>100)throw new IllegalArgumentException("Score out of range"); return new Outcome(p.getFileName().toString(),true,"score="+score);}catch(Exception e){return new Outcome(p.getFileName().toString(),false,e.getClass().getSimpleName()+": "+e.getMessage());}}
 public static void main(String[] args)throws Exception{
  Path dir=Files.createTempDirectory("results"); for(int i=1;i<=8;i++)Files.writeString(dir.resolve("student"+i+".txt"),i==3?"bad":String.valueOf(i*10));
  List<Path> files=new ArrayList<>();try(var st=Files.list(dir)){st.forEach(files::add);} files.add(dir.resolve("missing.txt"));
  int poolSize=args.length==0?4:Integer.parseInt(args[0]); ExecutorService pool=Executors.newFixedThreadPool(poolSize); List<Future<Outcome>> futures=new ArrayList<>();
  for(Path p:files)futures.add(pool.submit(()->process(p))); int ok=0,fail=0;
  for(Future<Outcome> f:futures){Outcome o=f.get();if(o.success()){ok++;System.out.println("OK "+o.file()+" "+o.detail());}else{fail++;System.out.println("FAILED "+o.file()+" "+o.detail());}}
  pool.shutdown();System.out.println("SUMMARY success="+ok+", failed="+fail+", total="+(ok+fail)+", pool="+poolSize);
 }
}
