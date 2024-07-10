(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[931],{1942:function(e,n,t){Promise.resolve().then(t.bind(t,7977))},7977:function(e,n,t){"use strict";t.d(n,{default:function(){return I}});var s,l,a=t(7437),r=t(2265),i=t(9386),c=t(20),o=t(9629),u=t(9139),d=t(964),h=t(3908),m=t(1272),x=t(4794);let p=[{name:"NAME",uid:"name"},{name:"STATUS",uid:"status"},{name:"AUTHENTICATION",uid:"authentication"},{name:"ACTIONS",uid:"actions"}];function g(e){let n=r.useCallback((n,t)=>{let s="warning";switch("AuthorizationSuccess"===n.status.stage?s="success":("AuthorizationFailed"===n.status.stage||!0===n.status.inputRequired)&&(s="danger"),t){case"name":var l,r,c;return(0,a.jsx)("div",{className:"flex",children:(0,a.jsxs)("div",{className:"flex flex-col",children:[(0,a.jsx)("p",{className:"text-bold text-sm capitalize",children:null!==(r=null!==(l=n.username)&&void 0!==l?l:n.name)&&void 0!==r?r:"<no username>"}),(0,a.jsx)("p",{className:"text-bold text-sm capitalize text-default-400",children:11===(c=n.phone).length?"+".concat(c[0],"-").concat(c.slice(1,4),"-").concat(c.slice(4,7),"-").concat(c.slice(7)):10===c.length?"".concat(c.slice(0,3),"-").concat(c.slice(3,6),"-").concat(c.slice(6)):7===c.length?"".concat(c.slice(0,3),"-").concat(c.slice(3)):c})]})});case"status":return(0,a.jsx)(i.z,{className:"capitalize",color:s,size:"sm",variant:"flat",children:n.status.stage});case"authentication":if("success"===s)return null;return(0,a.jsx)(x.A,{isLoading:"warning"===s,onClick:()=>{e.onProvideClicked(n)},children:"Provide"});case"actions":return(0,a.jsx)("div",{className:"relative flex items-center gap-2"})}},[]);return(0,a.jsxs)(c.b,{"aria-label":"Example table with custom cells",children:[(0,a.jsx)(o.J,{columns:p,children:e=>(0,a.jsx)(u.j,{align:"actions"===e.uid?"center":"start",children:e.name},e.uid)}),(0,a.jsx)(d.y,{items:e.users,children:e=>(0,a.jsxs)(h.g,{children:[(0,a.jsx)(m.X,{children:n(e,"name")}),(0,a.jsx)(m.X,{children:n(e,"status")}),(0,a.jsx)(m.X,{children:n(e,"authentication")}),(0,a.jsx)(m.X,{children:n(e,"actions")})]},e.phone)})]})}class j{static getInstance(){return j.instance||(j.instance=new j),j.instance}async request(e,n){try{let t=await fetch("".concat(this.baseURL).concat(e),n),s=await t.json();if(!t.ok)return{success:!1,error:s.error||"Unknown error occurred"};return{success:!0,data:s}}catch(e){return{success:!1,error:e instanceof Error?e.message:"Unknown error occurred"}}}async getClients(e){return e?this.request("/clients?hash="+e):this.request("/clients")}async submitValue(e,n,t){return this.request("/submitvalue",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({phone:e,stage:n,value:t})})}async addAccount(e,n,t){return this.request("/addtgaccount",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({phone_number:e,email:n,comment:t})})}constructor(){let e=window.location.protocol,n=window.location.hostname,t="https:"===e?"https":"http";if("localhost"===n)this.baseURL="".concat(t,"://localhost:8888");else{let e=window.location.port;""==e?this.baseURL="".concat(t,"://").concat(n):this.baseURL="".concat(t,"://").concat(n,":").concat(e)}}}var f=t(9834),b=t(9991),v=t(5448),C=t(6801),y=t(1496),S=t(9960),w=t(5256),E=t(1025),R=t(7971),A=t(5410),O=t(5286);let N={PasswordRequired:{name:"PasswordRequired",inputType:"text",label:"Password",placeholder:"Enter the account password"},AuthCodeRequired:{name:"AuthCodeRequired",inputType:"text",label:"Auth Code",placeholder:"Enter the Telegram auth code"},EmailCodeRequired:{name:"EmailCodeRequired",inputType:"text",label:"E-mail code",placeholder:"Enter code from email"}};function P(e){let{isOpen:n,onOpenChange:t}=(0,C.q)({isOpen:e.isOpen}),s=e.isOpen?N[e.user.status.stage]:null;return(0,a.jsx)(y.R,{isOpen:n,onOpenChange:t,onClose:()=>{e.onClose()},children:(0,a.jsx)(S.A,{children:n=>(0,a.jsxs)(a.Fragment,{children:[(0,a.jsx)(w.k,{className:"flex flex-col gap-1",children:e.user.status.stage}),e.submitting?(0,a.jsxs)(a.Fragment,{children:[(0,a.jsx)(E.I,{children:"Submitting..."}),(0,a.jsx)(R.R,{children:(0,a.jsx)(b.c,{})})]}):(0,a.jsxs)(a.Fragment,{children:[(0,a.jsxs)(E.I,{children:[(0,a.jsx)("p",{children:"Please enter the thingy."}),(0,a.jsx)("div",{children:(0,a.jsx)(O.Y,{isRequired:!0,type:s.inputType,label:s.label,placeholder:s.placeholder,value:e.inputValue[0],onValueChange:n=>{e.inputValue[1](n)}})})]}),(0,a.jsxs)(R.R,{children:[(0,a.jsx)(A.A,{color:"danger",variant:"light",onPress:n,children:"Close"}),(0,a.jsx)(A.A,{color:"primary",onPress:()=>{var n;n=e.inputValue[0],e.onSubmit(n)},children:"Submit"})]})]})]})})})}function T(e){return e&&e.length>0?e:null}function q(e){let{isOpen:n,onOpenChange:t}=(0,C.q)({isOpen:!0}),[s,l]=(0,r.useState)(!1),[i,c]=(0,r.useState)(""),[o,u]=(0,r.useState)(""),[d,h]=(0,r.useState)("");return(0,a.jsx)(y.R,{isOpen:n,isDismissable:!s,onOpenChange:t,onClose:()=>{e.onClose()},children:(0,a.jsx)(S.A,{children:n=>(0,a.jsxs)(a.Fragment,{children:[(0,a.jsx)(w.k,{className:"flex flex-col gap-1",children:"Add Telegram Account"}),s?(0,a.jsxs)(a.Fragment,{children:[(0,a.jsx)(E.I,{children:"Submitting..."}),(0,a.jsx)(R.R,{children:(0,a.jsx)(b.c,{})})]}):(0,a.jsxs)(a.Fragment,{children:[(0,a.jsx)(E.I,{children:(0,a.jsxs)("div",{className:"flex flex-col gap-6",children:[(0,a.jsx)(O.Y,{isRequired:!0,type:"text",label:"Phone number",placeholder:"Enter  phone number...",labelPlacement:"outside",maxLength:11,pattern:"d{11}",value:i,onValueChange:e=>{c(e)}}),(0,a.jsx)(O.Y,{isRequired:!1,type:"email",label:"E-mail",placeholder:"Enter email...",labelPlacement:"outside",maxLength:255,value:o,onValueChange:e=>{u(e)}}),(0,a.jsx)(O.Y,{isRequired:!1,type:"text",label:"Comment",placeholder:"Account belongs to...",labelPlacement:"outside",maxLength:300,value:d,onValueChange:e=>{h(e)}})]})}),(0,a.jsxs)(R.R,{children:[(0,a.jsx)(A.A,{color:"danger",variant:"light",onPress:n,children:"Close"}),(0,a.jsx)(A.A,{color:"primary",onPress:()=>{l(!0),e.onSubmit({phone:i,email:T(o),comment:T(d)})},children:"Submit"})]})]})]})})})}function k(e){let{isOpen:n,onOpenChange:t}=(0,C.q)({isOpen:e.isOpen});return(0,a.jsx)(y.R,{isOpen:n,onOpenChange:t,onClose:e.onClose,children:(0,a.jsx)(S.A,{children:n=>(0,a.jsxs)(a.Fragment,{children:[(0,a.jsx)(w.k,{className:"flex flex-col gap-1",children:e.title}),(0,a.jsx)(E.I,{children:(0,a.jsx)("p",{children:e.message})}),(0,a.jsx)(R.R,{children:(0,a.jsx)(A.A,{color:"primary",onPress:n,children:"Close"})})]})})})}function I(){var e,n;let[t,s]=(0,r.useState)(null),l=(0,r.useRef)(null),[i,c]=(0,r.useState)(!1),[o,u]=(0,r.useState)(!1),[d,h]=(0,r.useState)(null),[m,p]=(0,r.useState)(!1),C=(0,r.useState)(""),[y,S]=(0,r.useState)(0),[w,E]=(0,r.useState)(null),R=(0,r.useCallback)(async()=>{if(!o){c(!0);try{let e=j.getInstance(),n=await e.getClients(l.current);n.success?(n.data.hash!==l.current&&s(n.data.items),l.current=n.data.hash):console.error("Error fetching from server: ".concat(n.error)),u(!n.success)}catch(e){console.error("Error fetching clients: ",e),u(!0)}finally{c(!1)}}},[o]);if(!function(e,n){let t=arguments.length>2&&void 0!==arguments[2]?arguments[2]:[];arguments.length>3&&void 0!==arguments[3]&&arguments[3];let s=function(){let e=(0,r.useRef)(!0);return(0,r.useEffect)(()=>{let n=()=>{e.current=!document.hidden};return document.addEventListener("visibilitychange",n),()=>{document.removeEventListener("visibilitychange",n)}},[]),e}();!function(e,n){let t=arguments.length>2&&void 0!==arguments[2]?arguments[2]:[],s=!(arguments.length>3)||void 0===arguments[3]||arguments[3],l=(0,r.useRef)(),a=(0,r.useRef)(!1),i=(0,r.useRef)(!1);(0,r.useEffect)(()=>{l.current=n},[n]);let c=(0,r.useCallback)(async()=>{if(!a.current){a.current=!0;try{var e;await (null===(e=l.current)||void 0===e?void 0:e.call(l))}finally{a.current=!1,i.current=!0}}},[]);(0,r.useEffect)(()=>{s?c():i.current=!0},[]),(0,r.useEffect)(()=>{if(null!==e){let n=setInterval(()=>{i.current&&c()},e);return()=>clearInterval(n)}},[e,c,...t])}(e,(0,r.useCallback)(async()=>{s.current&&await n()},[n]),t)}(5e3,R,[R]),o)return(0,a.jsx)(f.w,{children:(0,a.jsx)(v.G,{children:"Failed to reach server. Please try again later."})});async function A(e){S(2);let n=await j.getInstance().addAccount(e.phone,e.email,e.comment);n.success||E({title:"Error",content:"Failed to add account: ".concat(n.error)}),S(0)}return(0,a.jsxs)(a.Fragment,{children:[0===y?null:(0,a.jsx)(q,{onClose:()=>{S(0)},onSubmit:e=>{A(e)}}),(0,a.jsxs)("div",{className:"flex flex-col gap-4",children:[(0,a.jsx)(k,{isOpen:null!=w,onClose:()=>{E(null)},title:null!==(e=null==w?void 0:w.title)&&void 0!==e?e:"",message:null!==(n=null==w?void 0:w.content)&&void 0!==n?n:""}),(0,a.jsx)(P,{submitting:m,isOpen:null!==d,onClose:()=>{h(null)},onSubmit:e=>{C[1](""),function(e){(async()=>{try{let n=j.getInstance();p(!0);let l=await n.submitValue(null==d?void 0:d.phone,null==d?void 0:d.status.stage,e);if(await new Promise(e=>setTimeout(e,2e3)),p(!1),l.success){if(null===t||null===d)return;let e=t.map(e=>e.phone===d.phone?{...e,status:{...e.status,inputRequired:!1}}:e);s(e)}else console.error("Error submitting code to server: ".concat(l.error)),u(!0)}catch(e){console.error("Error submitting code to server: ",e),u(!0)}h(null)})()}(e)},inputValue:C,user:d}),null===t?(0,a.jsx)(f.w,{children:(0,a.jsx)(v.G,{children:"Waiting for data..."})}):(0,a.jsxs)(a.Fragment,{children:[(0,a.jsxs)("div",{className:"flex gap-4 justify-between",children:[(0,a.jsx)("span",{}),(0,a.jsx)(x.A,{size:"sm",onClick:()=>{S(1)},children:"Add Account"})]}),(0,a.jsx)(g,{users:t,onProvideClicked:function(e){h(e)}})]})]}),(0,a.jsx)("div",{children:i&&(0,a.jsx)(b.c,{})})]})}(s=l||(l={}))[s.CLOSED=0]="CLOSED",s[s.OPEN=1]="OPEN",s[s.SUBMITTING=2]="SUBMITTING"}},function(e){e.O(0,[974,420,971,23,744],function(){return e(e.s=1942)}),_N_E=e.O()}]);