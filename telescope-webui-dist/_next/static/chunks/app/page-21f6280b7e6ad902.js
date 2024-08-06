(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[931],{1942:function(e,n,s){Promise.resolve().then(s.bind(s,748))},748:function(e,n,s){"use strict";s.d(n,{default:function(){return B}});var t,l,c=s(7437),a=s(2265),r=s(9386),o=s(8740),i=s(9629),u=s(9139),d=s(964),h=s(3908),x=s(1272),m=s(4794);function p(e){var n,s,t;let l=e.user;return(0,c.jsxs)("div",{className:"flex flex-col",children:[(0,c.jsx)("p",{className:"text-bold text-sm",children:null!==(s=null!==(n=l.username)&&void 0!==n?n:l.name)&&void 0!==s?s:"<no username>"}),(0,c.jsx)("p",{className:"text-bold text-sm text-default-400",children:11===(t=l.phone).length?"+".concat(t[0],"-").concat(t.slice(1,4),"-").concat(t.slice(4,7),"-").concat(t.slice(7)):10===t.length?"".concat(t.slice(0,3),"-").concat(t.slice(3,6),"-").concat(t.slice(6)):7===t.length?"".concat(t.slice(0,3),"-").concat(t.slice(3)):t}),(0,c.jsx)("p",{className:"text-bold text-sm text-default-400",children:l.email}),(0,c.jsx)("p",{className:"text-bold text-sm text-default-400",children:l.comment})]})}let g=[{name:"NAME",uid:"name"},{name:"STATUS",uid:"status"},{name:"AUTHENTICATION",uid:"authentication"},{name:"ACTIONS",uid:"actions"}];function f(e){let n=a.useCallback((n,s)=>{let t="warning";switch("AuthorizationSuccess"===n.status.stage?t="success":"ClientNotStarted"===n.status.stage?t="default":("ConnectionClosed"===n.status.stage||"ErrorOccurred"===n.status.stage||!0===n.status.inputRequired)&&(t="danger"),s){case"name":return(0,c.jsx)("div",{className:"flex",children:(0,c.jsx)("div",{className:"flex flex-col",children:(0,c.jsx)(p,{user:n})})});case"status":return(0,c.jsx)(r.z,{className:"capitalize",color:t,size:"sm",variant:"flat",children:n.status.stage});case"authentication":if(null!==n.status.error)return(0,c.jsx)("p",{children:n.status.error});if("success"===t||!n.status.inputRequired)return null;return(0,c.jsx)(m.A,{isLoading:"warning"===t,onClick:()=>{e.onProvideClicked(n)},children:"Provide"});case"actions":return(0,c.jsx)("div",{className:"relative flex items-center gap-2",children:e.renderActionButtons(n)})}},[]);return(0,c.jsxs)(o.b,{"aria-label":"Example table with custom cells",children:[(0,c.jsx)(i.J,{columns:g,children:e=>(0,c.jsx)(u.j,{align:"actions"===e.uid?"center":"start",children:e.name},e.uid)}),(0,c.jsx)(d.y,{items:e.users,children:e=>(0,c.jsxs)(h.g,{children:[(0,c.jsx)(x.X,{children:n(e,"name")}),(0,c.jsx)(x.X,{children:n(e,"status")}),(0,c.jsx)(x.X,{children:n(e,"authentication")}),(0,c.jsx)(x.X,{children:n(e,"actions")})]},e.phone)})]})}class j{static getInstance(){return j.instance||(j.instance=new j),j.instance}async request(e,n){try{let s=await fetch("".concat(this.baseURL).concat(e),n),t=await s.json();if(!s.ok)return{success:!1,error:t.error||"Unknown error occurred"};return{success:!0,data:t}}catch(e){return{success:!1,error:e instanceof Error?e.message:"Unknown error occurred"}}}async getClients(e){return e?this.request("/clients?hash="+e):this.request("/clients")}async connectClient(e){return this.request("/tgconnect?phone="+e)}async disconnectClient(e){return this.request("/tgdisconnect?phone="+e)}async deleteaccount(e){return this.request("/deleteaccount?phone="+e)}async submitValue(e,n,s){return this.request("/submitvalue",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({phone:e,stage:n,value:s})})}async addAccount(e,n,s){return this.request("/addtgaccount",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({phone_number:e,email:n,comment:s})})}constructor(){let e=window.location.protocol,n=window.location.hostname,s="https:"===e?"https":"http";if("localhost"===n)this.baseURL="".concat(s,"://localhost:8888");else{let e=window.location.port;""==e?this.baseURL="".concat(s,"://").concat(n):this.baseURL="".concat(s,"://").concat(n,":").concat(e)}}}var C=s(9834),v=s(8941),b=s(9991),y=s(5448),w=s(6801),A=s(1496),E=s(9960),R=s(5256),O=s(1025),S=s(7971),P=s(1094),N=s(5286);let k={PasswordRequired:{name:"PasswordRequired",inputType:"text",label:"Password",placeholder:"Enter the account password",filter_regex:/\s/g,validate:e=>e.length>0?null:"Cannot be empty."},AuthCodeRequired:{name:"AuthCodeRequired",inputType:"text",label:"Auth Code",placeholder:"Enter the Telegram auth code",maxLength:5,filter_regex:/\D/g,validate:e=>/^[0-9]{5}$/.test(e)?null:"Auth code is exactly 5 digits."},EmailCodeRequired:{name:"EmailCodeRequired",inputType:"text",label:"E-mail code",placeholder:"Enter code from email",filter_regex:/\s/g,validate:e=>e.length>0?null:"Must enter an email code."}};function T(e){let{isOpen:n,onOpenChange:s}=(0,w.q)({isOpen:e.isOpen}),t=e.isOpen?k[e.user.status.stage]:null,l=null;return null!==t&&(null==t?void 0:t.validate)!==null&&(l=t.validate(e.value)),(0,c.jsx)(A.R,{isOpen:n,onOpenChange:s,onClose:()=>{e.onClose()},children:(0,c.jsx)(E.A,{children:n=>(0,c.jsxs)(c.Fragment,{children:[(0,c.jsx)(R.k,{className:"flex flex-col gap-1",children:e.user.status.stage}),e.submitting?(0,c.jsxs)(c.Fragment,{children:[(0,c.jsx)(O.I,{children:"Submitting..."}),(0,c.jsx)(S.R,{children:(0,c.jsx)(b.c,{})})]}):(0,c.jsxs)(c.Fragment,{children:[(0,c.jsxs)(O.I,{children:[(0,c.jsx)("p",{children:"Please enter the thingy."}),(0,c.jsx)("div",{children:(0,c.jsx)(N.Y,{isRequired:!0,type:t.inputType,label:t.label,placeholder:t.placeholder,maxLength:null==t?void 0:t.maxLength,isInvalid:null!==l,color:null!==l?"danger":"success",errorMessage:null!=l?l:"",value:e.value,onValueChange:n=>{(null==t?void 0:t.filter_regex)?e.setValue(n.replaceAll(t.filter_regex,"")):e.setValue(n)}})})]}),(0,c.jsxs)(S.R,{children:[(0,c.jsx)(P.A,{color:"danger",variant:"light",onPress:n,children:"Close"}),(0,c.jsx)(P.A,{color:"primary",onPress:()=>{var n;n=e.value,e.onSubmit(n)},children:"Submit"})]})]})]})})})}function q(e){return e&&e.length>0?e:null}function I(e){let{isOpen:n,onOpenChange:s}=(0,w.q)({isOpen:!0}),[t,l]=(0,a.useState)(!1),[r,o]=(0,a.useState)(""),[i,u]=(0,a.useState)(""),[d,h]=(0,a.useState)("");return(0,c.jsx)(A.R,{isOpen:n,isDismissable:!t,onOpenChange:s,onClose:()=>{e.onClose()},children:(0,c.jsx)(E.A,{children:n=>(0,c.jsxs)(c.Fragment,{children:[(0,c.jsx)(R.k,{className:"flex flex-col gap-1",children:"Add Telegram Account"}),t?(0,c.jsxs)(c.Fragment,{children:[(0,c.jsx)(O.I,{children:"Submitting..."}),(0,c.jsx)(S.R,{children:(0,c.jsx)(b.c,{})})]}):(0,c.jsxs)(c.Fragment,{children:[(0,c.jsx)(O.I,{children:(0,c.jsxs)("div",{className:"flex flex-col gap-6",children:[(0,c.jsx)(N.Y,{isRequired:!0,type:"text",label:"Phone number",placeholder:"Enter phone number...",labelPlacement:"outside",maxLength:11,pattern:"d{11}",value:r,onValueChange:e=>{o(e)}}),(0,c.jsx)(N.Y,{isRequired:!1,type:"email",label:"E-mail",placeholder:"Enter email...",labelPlacement:"outside",maxLength:255,value:i,onValueChange:e=>{u(e)}}),(0,c.jsx)(N.Y,{isRequired:!1,type:"text",label:"Comment",placeholder:"Account belongs to...",labelPlacement:"outside",maxLength:300,value:d,onValueChange:e=>{h(e)}})]})}),(0,c.jsxs)(S.R,{children:[(0,c.jsx)(P.A,{color:"danger",variant:"light",onPress:n,children:"Close"}),(0,c.jsx)(P.A,{color:"primary",onPress:()=>{l(!0),e.onSubmit({phone:r,email:q(i),comment:q(d)})},children:"Submit"})]})]})]})})})}function F(e){let{isOpen:n,onOpenChange:s}=(0,w.q)({isOpen:e.isOpen});return(0,c.jsx)(A.R,{isOpen:n,onOpenChange:s,onClose:e.onClose,children:(0,c.jsx)(E.A,{children:n=>(0,c.jsxs)(c.Fragment,{children:[(0,c.jsx)(R.k,{className:"flex flex-col gap-1",children:e.title}),(0,c.jsx)(O.I,{children:(0,c.jsx)("p",{children:e.message})}),(0,c.jsx)(S.R,{children:e.buttons.map(e=>(0,c.jsx)(P.A,{color:e.color,onPress:()=>{e.onPress(e.key)},children:e.label}))})]})})})}let L=[{unit:"year",seconds:31104e3},{unit:"month",seconds:2592e3},{unit:"day",seconds:86400},{unit:"hour",seconds:3600},{unit:"minute",seconds:60},{unit:"second",seconds:1}];var D=s(9726),U=s(6356),V=s(4983),_=s(1810);function M(e){let{isOpen:n,onOpenChange:s}=(0,w.q)({isOpen:e.isOpen}),[t,l]=(0,a.useState)("");return(0,c.jsx)(A.R,{isOpen:n,onOpenChange:s,onClose:e.onClose,children:(0,c.jsx)(E.A,{children:n=>(0,c.jsxs)(c.Fragment,{children:[(0,c.jsx)(R.k,{className:"flex flex-col gap-1",children:"Remove account"}),(0,c.jsxs)(O.I,{children:[(0,c.jsx)("p",{children:"Really remove this account from Telescope and delete all associated data?"}),(0,c.jsx)("div",{className:"flex items-center ml-6",children:(0,c.jsx)(p,{user:e.user})})]}),(0,c.jsx)(S.R,{children:(0,c.jsxs)("div",{className:"w-full flex flex-col gap-3",children:[(0,c.jsx)("div",{children:(0,c.jsx)(N.Y,{isRequired:!0,type:"text",label:"Confirm",placeholder:"Type DELETE to confirm...",labelPlacement:"outside",maxLength:6,value:t,onValueChange:e=>{l(e.toUpperCase())}})}),(0,c.jsxs)("div",{className:"flex flex-row gap-2",children:[(0,c.jsx)(P.A,{color:"danger",isDisabled:"DELETE"!=t.toUpperCase(),onPress:()=>{l(""),e.onConfirmed(e.user)},children:"Delete User"}),(0,c.jsx)(P.A,{color:"default",onPress:()=>{e.onClose()},children:"Cancel"})]})]})})]})})})}let Y=/\s/g;function z(e){let{isOpen:n,onOpenChange:s}=(0,w.q)({isOpen:e.isOpen}),[t,l]=(0,a.useState)(""),[r,o]=(0,a.useState)(""),i=null;return 0==t.length?i="Must enter a 2FA password.":t!=r&&(i="Password and confirm field must match."),(0,c.jsx)(A.R,{isOpen:n,onOpenChange:s,onClose:e.onClose,children:(0,c.jsx)(E.A,{children:n=>(0,c.jsxs)(c.Fragment,{children:[(0,c.jsx)(R.k,{className:"flex flex-col gap-1",children:"Edit 2FA password"}),(0,c.jsxs)(O.I,{children:[(0,c.jsx)("p",{children:"You are submitting a new 2FA password for the following account:"}),(0,c.jsx)("div",{className:"flex items-center ml-6",children:(0,c.jsx)(p,{user:e.user})})]}),(0,c.jsx)(S.R,{children:(0,c.jsxs)("div",{className:"w-full flex flex-col gap-6",children:[(0,c.jsxs)("div",{className:"flex flex-col gap-2",children:[(0,c.jsx)(N.Y,{isRequired:!0,type:"password",label:"2FA Password",placeholder:"Please enter the password...",labelPlacement:"outside",value:t,onValueChange:e=>{l(e.replaceAll(Y,""))}}),(0,c.jsx)(N.Y,{isRequired:!0,type:"password",label:"Confirm",placeholder:"Please confirm the password...",labelPlacement:"outside",value:r,onValueChange:e=>{o(e.replaceAll(Y,""))}})]}),(0,c.jsxs)("div",{className:"flex flex-row gap-2",children:[(0,c.jsx)(v.e,{content:null!=i?i:"",isDisabled:null===i,children:(0,c.jsx)("span",{children:(0,c.jsx)(P.A,{color:"danger",isDisabled:0==t.length||t!=r,onPress:()=>{l(""),o(""),e.onSubmit(e.user,t)},children:"Change Password"})})}),(0,c.jsx)(P.A,{color:"default",onPress:()=>{e.onClose()},children:"Cancel"})]})]})})]})})})}function B(){let[e,n]=(0,a.useState)(null),s=(0,a.useRef)(null),[t,l]=(0,a.useState)(!1),[r,o]=(0,a.useState)(!1),[i,u]=(0,a.useState)(null),[d,h]=(0,a.useState)(!1),[x,p]=(0,a.useState)(""),[g,w]=(0,a.useState)(0),[A,E]=(0,a.useState)(null),[R,O]=(0,a.useState)(null),[S,P]=(0,a.useState)(null),N=(0,a.useCallback)(async()=>{if(!r){l(!0);try{let e=j.getInstance(),t=await e.getClients(s.current);t.success?(t.data.hash!==s.current&&n(t.data.items),s.current=t.data.hash):console.error("Error fetching from server: ".concat(t.error)),o(!t.success)}catch(e){console.error("Error fetching clients: ",e),o(!0)}finally{l(!1)}}},[r]);if(!function(e,n){let s=arguments.length>2&&void 0!==arguments[2]?arguments[2]:[];arguments.length>3&&void 0!==arguments[3]&&arguments[3];let t=function(){let e=(0,a.useRef)(!0);return(0,a.useEffect)(()=>{let n=()=>{e.current=!document.hidden};return document.addEventListener("visibilitychange",n),()=>{document.removeEventListener("visibilitychange",n)}},[]),e}();!function(e,n){let s=arguments.length>2&&void 0!==arguments[2]?arguments[2]:[],t=!(arguments.length>3)||void 0===arguments[3]||arguments[3],l=(0,a.useRef)(),c=(0,a.useRef)(!1),r=(0,a.useRef)(!1);(0,a.useEffect)(()=>{l.current=n},[n]);let o=(0,a.useCallback)(async()=>{if(!c.current){c.current=!0;try{var e;await (null===(e=l.current)||void 0===e?void 0:e.call(l))}finally{c.current=!1,r.current=!0}}},[]);(0,a.useEffect)(()=>{t?o():r.current=!0},[]),(0,a.useEffect)(()=>{if(null!==e){let n=setInterval(()=>{r.current&&o()},e);return()=>clearInterval(n)}},[e,o,...s])}(e,(0,a.useCallback)(async()=>{t.current&&await n()},[n]),s)}(5e3,N,[N]),r)return(0,c.jsx)(C.w,{children:(0,c.jsx)(y.G,{children:"Failed to reach server. Please try again later."})});async function k(e){w(2);let n=await j.getInstance().addAccount(e.phone,e.email,e.comment);n.success||q("Error","Failed to add account: ".concat(n.error)),w(0)}function q(e,n){E({title:e,message:n,onClose:()=>{E(null)},buttons:[{key:"okay",label:"Okay",color:"primary",onPress:()=>{E(null)}}]})}return(0,c.jsxs)(c.Fragment,{children:[0===g?null:(0,c.jsx)(I,{onClose:()=>{w(0)},onSubmit:e=>{k(e)}}),(0,c.jsxs)("div",{className:"flex flex-col gap-4",children:[(0,c.jsx)(M,{isOpen:null!=R,user:R,onClose:()=>{O(null)},onConfirmed:e=>{O(null),async function(){let n=await j.getInstance().deleteaccount(e.phone);n.success||q("Error","Failed to delete account: ".concat(n.error))}()}}),(0,c.jsx)(z,{isOpen:null!=S,user:S,onClose:()=>{P(null)},onSubmit:(e,n)=>{P(null)}}),(0,c.jsx)(F,{isOpen:null!=A,...null!==A?A:{title:"",message:"",buttons:[],onClose:()=>{}}}),(0,c.jsx)(T,{submitting:d,isOpen:null!==i,onClose:()=>{u(null)},onSubmit:s=>{p(""),function(s){(async()=>{try{let t=j.getInstance();h(!0);let l=null==i?void 0:i.status.stage,c=await t.submitValue(null==i?void 0:i.phone,null==i?void 0:i.status.stage,s);if(await new Promise(e=>setTimeout(e,2e3)),h(!1),c.success){if(null===e||null===i)return;let s=e.map(e=>e.phone===i.phone&&e.status.stage===l?{...e,status:{...e.status,inputRequired:!1}}:e);n(s)}else console.error("Error submitting code to server: ".concat(c.error)),o(!0)}catch(e){console.error("Error submitting code to server: ",e),o(!0)}u(null)})()}(s)},value:x,setValue:p,user:i}),null===e?(0,c.jsx)(C.w,{children:(0,c.jsx)(y.G,{children:"Waiting for data..."})}):(0,c.jsxs)(c.Fragment,{children:[(0,c.jsxs)("div",{className:"flex gap-4 justify-between",children:[(0,c.jsx)("span",{}),(0,c.jsx)(m.A,{size:"sm",onClick:()=>{w(1)},children:"Add Account"})]}),(0,c.jsx)(f,{users:e,onProvideClicked:function(e){u(e)},renderActionButtons:e=>(0,c.jsxs)(_.Pd.Provider,{value:{size:"19px"},children:[(0,c.jsx)(v.e,{content:"Retrieve auth code",children:(0,c.jsx)(m.A,{isIconOnly:!0,color:"default","aria-label":"Retrieve auth code",isDisabled:!e.lastCode,onClick:()=>{var n;q("Auth code","As of ".concat((n=e.lastCode.date,function(e){for(let{unit:n,seconds:s}of L)if(e>=s){let t=Math.floor(e/s);return"".concat(t," ").concat(n).concat(1!==t?"s":"")}return"0 seconds"}(Math.floor(Date.now()/1e3)-n))," ago the login code is: ").concat(e.lastCode.value))},children:(0,c.jsx)(V.dgU,{})})}),"ClientNotStarted"===e.status.stage?(0,c.jsx)(v.e,{content:"Connect Telegram session for this account",children:(0,c.jsx)(m.A,{isIconOnly:!0,color:"default","aria-label":"Connect Telegram session for this account",onClick:()=>{j.getInstance().connectClient(e.phone).then(n=>{n.success?q("Success","Connected account ".concat(e.phone,".")):q("Error","Couldn't connect account ".concat(e.phone,": ").concat(n.error))})},children:(0,c.jsx)(U.y6x,{})})}):(0,c.jsx)(v.e,{content:"Disconnect currently active Telegram session",children:(0,c.jsx)(m.A,{isIconOnly:!0,color:"default","aria-label":"Disconnect currently active Telegram session",onClick:()=>{E({title:"Disconnect",message:"Really disconnect ".concat(e.phone,"?"),onClose:()=>{E(null)},buttons:[{key:"disconnect",label:"Disconnect",color:"danger",onPress:()=>{E(null),j.getInstance().disconnectClient(e.phone).then(n=>{n.success?q("Success","Disconnected account ".concat(e.phone,".")):q("Error","Couldn't disconnect account ".concat(e.phone,": ").concat(n.error))})}},{key:"cancel",label:"Cancel",color:"default",onPress:()=>{E(null)}}]})},children:(0,c.jsx)(D.ZUl,{className:"font-bold"})})}),(0,c.jsx)(v.e,{content:"Edit account's 2FA password",children:(0,c.jsx)(m.A,{isIconOnly:!0,"aria-label":"Edit account's 2FA password",onClick:()=>{P(e)},children:(0,c.jsx)(U.U$P,{})})}),(0,c.jsx)(v.e,{content:"Remove account from Telescope",children:(0,c.jsx)(m.A,{isIconOnly:!0,color:"danger","aria-label":"Remove account from Telescope",onClick:()=>{O(e)},children:(0,c.jsx)(U.FH3,{})})})]})})]})]}),(0,c.jsx)("div",{children:t&&(0,c.jsx)(b.c,{})})]})}(t=l||(l={}))[t.CLOSED=0]="CLOSED",t[t.OPEN=1]="OPEN",t[t.SUBMITTING=2]="SUBMITTING"}},function(e){e.O(0,[217,821,51,265,798,971,23,744],function(){return e(e.s=1942)}),_N_E=e.O()}]);