<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { api, authHeader } from './api'
type Facility={id:number,name:string,building:string,capacity:number,equipment:string[]}
type Booking={id:number,facility:number,facility_name:string,purpose:string,start_at:string,end_at:string,status:string}
type Ticket={id:number,title:string,facility:number,facility_name:string,priority:string,status:string,description:string}
const username=ref('student'), password=ref('CampusDemo123!')
const logged=ref(false), loading=ref(false), error=ref(''), notice=ref('')
const facilities=ref<Facility[]>([]), bookings=ref<Booking[]>([]), tickets=ref<Ticket[]>([])
const active=ref('overview')
const bookingForm=ref({facility:'',purpose:'Laboratory session',start_at:'',end_at:''})
const ticketForm=ref({facility:'',title:'Projector not working',description:'',priority:'MEDIUM'})
const headers=computed(()=>authHeader(username.value,password.value))
async function loadPublic(){try{facilities.value=(await api.get('/facilities/')).data.results ?? (await api.get('/facilities/')).data}catch(e){/* backend may not yet be running */}}
async function login(){error.value='';loading.value=true;try{await api.get('/bookings/',headers.value);logged.value=true;await loadPrivate()}catch(e:any){error.value=e?.response?.status===401?'Login failed. Check Django user credentials.':'Cannot reach API. Start Docker Compose and create a demo user.'}finally{loading.value=false}}
async function loadPrivate(){try{const [b,t]=await Promise.all([api.get('/bookings/',headers.value),api.get('/tickets/',headers.value)]);bookings.value=b.data.results??b.data;tickets.value=t.data.results??t.data}catch(e:any){error.value='Could not load records. Check API and account role.'}}
async function createBooking(){error.value='';notice.value='';try{await api.post('/bookings/',{...bookingForm.value,facility:Number(bookingForm.value.facility)},headers.value);notice.value='Booking request submitted.';await loadPrivate()}catch(e:any){error.value=e?.response?.data?.detail||JSON.stringify(e?.response?.data)||'Booking failed.'}}
async function createTicket(){error.value='';try{await api.post('/tickets/',{...ticketForm.value,facility:Number(ticketForm.value.facility)},headers.value);notice.value='Maintenance ticket submitted.';await loadPrivate()}catch(e:any){error.value=JSON.stringify(e?.response?.data)||'Ticket failed.'}}
async function transitionBooking(id:number,target:string){try{await api.post(`/bookings/${id}/transition/`,{target},headers.value);notice.value=`Booking ${target.toLowerCase()}.`;await loadPrivate()}catch(e:any){error.value=JSON.stringify(e?.response?.data)||'Transition rejected.'}}
async function transitionTicket(id:number,target:string){try{await api.post(`/tickets/${id}/transition/`,{target},headers.value);notice.value=`Ticket ${target.toLowerCase()}.`;await loadPrivate()}catch(e:any){error.value=JSON.stringify(e?.response?.data)||'Transition rejected.'}}
onMounted(loadPublic)
</script>

<template>
<div class="shell">
  <aside class="sidebar">
    <div class="brand"><div class="brandmark">C</div><div><b>CampusOps</b><small>SMART FACILITY PLATFORM</small></div></div>
    <div class="navlabel">WORKSPACE</div>
    <button v-for="item in [{id:'overview',name:'Overview',icon:'▦'},{id:'bookings',name:'Bookings',icon:'▣'},{id:'tickets',name:'Maintenance',icon:'⚙'}]" :key="item.id" :class="{selected:active===item.id}" @click="active=item.id">{{item.icon}} <span>{{item.name}}</span></button>
    <div class="sidefoot">SIMATS Engineering<br><small>Assignment 3 · CO3</small></div>
  </aside>
  <main class="main">
    <header><div><p class="eyebrow">CAMPUS OPERATIONS / {{active.toUpperCase()}}</p><h1>{{active==='overview'?'Operations dashboard':active==='bookings'?'Facility bookings':'Maintenance queue'}}</h1></div><div class="userpill"><span class="online"></span>{{logged?username:'Guest / demo'}}</div></header>
    <section v-if="!logged" class="login card">
      <div><p class="eyebrow">SECURE WORKSPACE</p><h2>Sign in to CampusOps</h2><p class="muted">Use a Django account created by the administrator.</p></div>
      <label>Username<input v-model="username" autocomplete="username"></label>
      <label>Password<input v-model="password" type="password" autocomplete="current-password"></label>
      <button class="primary" :disabled="loading" @click="login">{{loading?'Checking…':'Sign in'}}</button>
      <p class="hint">Demo account after setup: student / CampusDemo123!</p>
    </section>
    <template v-else>
      <div v-if="error" class="alert">{{error}}</div><div v-if="notice" class="notice">{{notice}}</div>
      <section v-if="active==='overview'" class="stats">
        <div class="card stat"><span>FACILITIES</span><strong>{{facilities.length}}</strong><small>Active spaces</small></div>
        <div class="card stat"><span>BOOKING REQUESTS</span><strong>{{bookings.length}}</strong><small>Visible to your role</small></div>
        <div class="card stat"><span>OPEN TICKETS</span><strong>{{tickets.filter(t=>t.status!=='CLOSED').length}}</strong><small>Maintenance workload</small></div>
      </section>
      <section class="grid">
        <div class="card">
          <div class="cardhead"><div><p class="eyebrow">RESOURCE CATALOGUE</p><h2>Available facilities</h2></div><span class="tag">LIVE API</span></div>
          <div v-for="f in facilities" :key="f.id" class="facility"><div class="facilityicon">⌂</div><div><b>{{f.name}}</b><small>{{f.building}} · Capacity {{f.capacity}}</small></div><span class="available">Active</span></div>
          <p v-if="!facilities.length" class="muted">No facilities seeded yet. Run the seed command in README.</p>
        </div>
        <div class="card formcard">
          <p class="eyebrow">REQUEST A SPACE</p><h2>New booking</h2>
          <label>Facility<select v-model="bookingForm.facility"><option value="">Choose facility</option><option v-for="f in facilities" :value="String(f.id)">{{f.name}}</option></select></label>
          <label>Purpose<input v-model="bookingForm.purpose"></label>
          <label>Start time<input type="datetime-local" v-model="bookingForm.start_at"></label>
          <label>End time<input type="datetime-local" v-model="bookingForm.end_at"></label>
          <button class="primary" @click="createBooking">Submit booking</button>
        </div>
      </section>
      <section v-if="active==='bookings'||active==='overview'" class="card tablecard">
        <div class="cardhead"><div><p class="eyebrow">SCHEDULING</p><h2>Recent bookings</h2></div><button class="ghost" @click="loadPrivate">Refresh</button></div>
        <div class="record" v-for="b in bookings" :key="b.id"><div><b>{{b.facility_name}}</b><small>{{b.purpose}} · {{new Date(b.start_at).toLocaleString()}}</small></div><span class="status">{{b.status}}</span><div class="actions"><button v-if="b.status==='REQUESTED'" @click="transitionBooking(b.id,'APPROVED')">Approve</button><button v-if="b.status==='APPROVED'" @click="transitionBooking(b.id,'CONFIRMED')">Confirm</button><button v-if="['REQUESTED','APPROVED','CONFIRMED'].includes(b.status)" @click="transitionBooking(b.id,'CANCELLED')">Cancel</button></div></div>
        <p v-if="!bookings.length" class="muted">No booking records yet.</p>
      </section>
      <section v-if="active==='tickets'||active==='overview'" class="grid lower">
        <div class="card">
          <div class="cardhead"><div><p class="eyebrow">SERVICE DESK</p><h2>Maintenance tickets</h2></div></div>
          <div class="record" v-for="t in tickets" :key="t.id"><div><b>{{t.title}}</b><small>{{t.facility_name}} · {{t.priority}}</small></div><span class="status">{{t.status}}</span><div class="actions"><button v-if="t.status==='OPEN'" @click="transitionTicket(t.id,'ASSIGNED')">Assign</button><button v-if="t.status==='ASSIGNED'" @click="transitionTicket(t.id,'IN_PROGRESS')">Start</button><button v-if="t.status==='IN_PROGRESS'" @click="transitionTicket(t.id,'RESOLVED')">Resolve</button><button v-if="t.status==='RESOLVED'" @click="transitionTicket(t.id,'CLOSED')">Close</button></div></div>
          <p v-if="!tickets.length" class="muted">No tickets reported.</p>
        </div>
        <div class="card formcard">
          <p class="eyebrow">REPORT AN ISSUE</p><h2>New ticket</h2>
          <label>Facility<select v-model="ticketForm.facility"><option value="">Choose facility</option><option v-for="f in facilities" :value="String(f.id)">{{f.name}}</option></select></label>
          <label>Title<input v-model="ticketForm.title"></label>
          <label>Description<textarea v-model="ticketForm.description"></textarea></label>
          <label>Priority<select v-model="ticketForm.priority"><option>LOW</option><option>MEDIUM</option><option>HIGH</option><option>CRITICAL</option></select></label>
          <button class="primary" @click="createTicket">Create ticket</button>
        </div>
      </section>
    </template>
    <div v-if="error&&!logged" class="alert">{{error}}</div>
    <footer>CampusOps · Version 1.0 · Academic prototype · Role-based API</footer>
  </main>
</div>
</template>
