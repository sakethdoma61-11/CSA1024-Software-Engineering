public class ThreadLifecycleDemo {
 static class Station extends Thread { private final int count; Station(String n,int c){super(n);count=c;} public void run(){try{Thread.sleep(40);System.out.println(getName()+" scanned "+count+" scripts");}catch(InterruptedException e){Thread.currentThread().interrupt();}} }
 public static void main(String[] args)throws InterruptedException {
  Thread[] stations={new Station("Station-1",25),new Station("Station-2",30),new Station("Station-3",20),new Station("Station-4",25)};
  for(Thread t:stations)t.start(); for(Thread t:stations)t.join();
  System.out.println("All stations completed; total scanned = 100");
 }
}
