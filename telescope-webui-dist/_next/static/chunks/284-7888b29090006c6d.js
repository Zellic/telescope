"use strict";(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[284],{4466:function(e,t,n){n.d(t,{J:function(){return s}});function s(){var e;let t=null===(e=document.cookie.split("; ").find(e=>e.startsWith("CF_Authorization=")))||void 0===e?void 0:e.split("=")[1];if(t){let e=t.split(".");if(e.length>0)return JSON.parse(atob(e[1])).email}return null}},3376:function(e,t,n){n.d(t,{s:function(){return s}});class s{static getInstance(){return s.instance||(s.instance=new s),s.instance}async request(e,t){try{let n=await fetch("".concat(this.baseURL).concat(e),t),s=await n.json();if(!n.ok)return{success:!1,error:s.error||"Unknown error occurred"};return{success:!0,data:s}}catch(e){return{success:!1,error:e instanceof Error?e.message:"Unknown error occurred"}}}async getClients(e){return e?this.request("/clients?hash="+e):this.request("/clients")}async getClient(e){return this.request("/getclient?phone="+e)}async connectClient(e){return this.request("/tgconnect?phone="+e)}async disconnectClient(e){return this.request("/tgdisconnect?phone="+e)}async deleteaccount(e){return this.request("/deleteaccount?phone="+e)}async setpassword(e,t){return this.request("/setpassword?phone="+e,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({password:t})})}async submitValue(e,t,n){return this.request("/submitvalue",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({phone:e,stage:t,value:n})})}async addAccount(e,t,n){return this.request("/addtgaccount",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({phone_number:e,email:t,comment:n})})}async addTestAccount(){return this.request("/addtestaccount")}constructor(){let e=window.location.protocol,t=window.location.hostname,n="https:"===e?"https":"http";if("localhost"===t)this.baseURL="".concat(n,"://localhost:8888");else{let e=window.location.port;""==e?this.baseURL="".concat(n,"://").concat(t):this.baseURL="".concat(n,"://").concat(t,":").concat(e)}}}},7040:function(e,t,n){n.d(t,{e:function(){return o}});var s=n(2265);function o(e,t){let n=arguments.length>2&&void 0!==arguments[2]?arguments[2]:[];arguments.length>3&&void 0!==arguments[3]&&arguments[3];let o=function(){let e=(0,s.useRef)(!0);return(0,s.useEffect)(()=>{let t=()=>{e.current=!document.hidden};return document.addEventListener("visibilitychange",t),()=>{document.removeEventListener("visibilitychange",t)}},[]),e}();!function(e,t){let n=arguments.length>2&&void 0!==arguments[2]?arguments[2]:[],o=!(arguments.length>3)||void 0===arguments[3]||arguments[3],a=(0,s.useRef)(),l=(0,s.useRef)(!1),c=(0,s.useRef)(!1);(0,s.useEffect)(()=>{a.current=t},[t]);let r=(0,s.useCallback)(async()=>{if(!l.current){l.current=!0;try{var e;await (null===(e=a.current)||void 0===e?void 0:e.call(a))}finally{l.current=!1,c.current=!0}}},[]);(0,s.useEffect)(()=>{o?r():c.current=!0},[]),(0,s.useEffect)(()=>{if(null!==e){let t=setInterval(()=>{c.current&&r()},e);return()=>clearInterval(t)}},[e,r,...n])}(e,(0,s.useCallback)(async()=>{o.current&&await t()},[t]),n)}},5691:function(e,t,n){n.d(t,{c:function(){return g},wm:function(){return v},no:function(){return f},gM:function(){return x}});var s=n(8890),o=n(2265),a=n(3376);let l=s.V5.enumeration("ActionType",["default","disconnect","add_test_account"]),c=s.V5.model({key:s.V5.string,label:s.V5.string,color:s.V5.maybeNull(s.V5.enumeration("Color",["default","primary","secondary","success","warning","danger"])),actionType:l}),r=s.V5.maybeNull(s.V5.reference(s.V5.late(()=>n(5691).c),{get(e,t){var n;return(null===(n=(0,s.yj)(t).clients)||void 0===n?void 0:n.find(t=>t.phone===e))||null},set:e=>e.phone})),i=s.V5.model({title:s.V5.string,message:s.V5.string,buttons:s.V5.array(c),client:r}),d=s.V5.model({addAccount:s.V5.maybeNull(s.V5.enumeration("AddAccountMode",["normal","onboarding"])),addAccountPhone:s.V5.maybeNull(s.V5.string),provide:r,editPassword:r,deleteClient:r,message:s.V5.maybeNull(i)}).actions(e=>({setProvideClient:function(t){e.provide=t},setEditPasswordClient:function(t){e.editPassword=t},setDeleteClient:function(t){e.deleteClient=t},setAddAccount:function(t){e.addAccount=t},setAddAccountPhone:function(t){e.addAccountPhone=t},setMessage:function(t,n,s,o){e.message=i.create({title:t,message:n,buttons:s,client:o||null})},setMessageBasic:function(t,n,s){e.message=i.create({title:t,message:n,buttons:[{key:"okay",label:"Okay",color:"primary",actionType:"default"}],client:s||null})},clearMessage:function(){e.message=null}}));var u=n(4466);let m=s.V5.model({stage:s.V5.enumeration("AuthState",["ClientNotStarted","WaitingOnServer","PasswordRequired","AuthCodeRequired","EmailRequired","EmailCodeRequired","AuthorizationSuccess","ConnectionClosed","ErrorOccurred","PhoneNumberRequired"]),inputRequired:s.V5.boolean,error:s.V5.maybeNull(s.V5.string)}),h=s.V5.enumeration("Privileges",["view","edit_two_factor_password","login","manage_connection_state","remove_account"]),g=s.V5.model({name:s.V5.maybeNull(s.V5.string),username:s.V5.maybeNull(s.V5.string),email:s.V5.maybeNull(s.V5.string),comment:s.V5.maybeNull(s.V5.string),phone:s.V5.string,lastCode:s.V5.maybeNull(s.V5.model({value:s.V5.number,date:s.V5.number})),status:m,privileges:s.V5.array(h)}).actions(e=>({updateStatus(t){e.status=m.create(t)}})),f=s.V5.model({userApiHash:s.V5.maybeNull(s.V5.string),clients:s.V5.array(g),cfClient:r,state:s.V5.enumeration("State",["pending","done","error"]),environment:s.V5.enumeration("Environment",["Staging","Production"]),modals:d}).actions(e=>({fetchClients:(0,s.ls)(function*(){try{let t=a.s.getInstance(),n=yield t.getClients(e.userApiHash);n.success?(n.data.hash!==e.userApiHash&&(e.clients=n.data.items||[],e.environment=n.data.environment),e.userApiHash=n.data.hash,e.state="done"):(console.error("Error fetching from server: ".concat(n.error)),e.state="error")}catch(t){console.error("Failed to fetch clients: ".concat(t)),e.state="error"}}),fetchClient:(0,s.ls)(function*(t){try{let n=a.s.getInstance(),s=yield n.getClient(t);s.success&&e.clients.replace([s.data.client])}catch(e){console.error("Failed to fetch client: ".concat(e))}}),updateCfClient:function(){null===e.cfClient&&(e.cfClient=e.clients.find(e=>e.email===(0,u.J)()))}})).create({clients:[],state:"pending",environment:"Production",modals:{}}),p=(0,o.createContext)(null),v=p.Provider;function x(){let e=(0,o.useContext)(p);if(null===e)throw Error("Store cannot be null, please add a context provider");return e}(0,s.cf)(f,e=>{console.log("snapshot",e)})},6283:function(e,t,n){n.d(t,{wQ:function(){return E},QB:function(){return P},gE:function(){return w},ZP:function(){return R}});var s=n(7437),o=n(5430),a=n(5691),l=n(9386),c=n(7265),r=n(9629),i=n(9139),d=n(964),u=n(3908),m=n(1272);function h(e){let t="warning";return"AuthorizationSuccess"===e.status.stage?t="success":"ClientNotStarted"===e.status.stage?t="default":("ConnectionClosed"===e.status.stage||"ErrorOccurred"===e.status.stage||!0===e.status.inputRequired)&&(t="danger"),t}n(2265);var g=n(4794),f=n(1810),p=n(8941);let v=[{unit:"year",seconds:31104e3},{unit:"month",seconds:2592e3},{unit:"day",seconds:86400},{unit:"hour",seconds:3600},{unit:"minute",seconds:60},{unit:"second",seconds:1}];var x=n(4983),b=n(3376),y=n(6356),C=n(9726);function j(e){return(0,s.jsx)(p.e,{content:e.content,children:(0,s.jsx)(g.A,{isIconOnly:!0,color:e.color||"default","aria-label":e.arialabel||e.content,onClick:e.onClick,isDisabled:e.disabled,children:(0,s.jsx)(e.icon,{className:e.iconClass})})})}let A=(0,o.Pi)(e=>{let{account:t,onboarding:n}=e,o=(0,a.gM)();return"ClientNotStarted"===t.status.stage?(0,s.jsx)(j,{content:"Connect Telegram session for this account",icon:y.y6x,disabled:n,onClick:()=>{b.s.getInstance().connectClient(t.phone).then(e=>{e.success?o.modals.setMessageBasic("Success","Connected account ".concat(t.phone,".")):o.modals.setMessageBasic("Error","Couldn't connect account ".concat(t.phone,": ").concat(e.error))})}}):(0,s.jsx)(j,{content:"Disconnect currently active Telegram session",icon:C.ZUl,iconClass:"font-bold",disabled:n,onClick:()=>{o.modals.setMessage("Disconnect","Really disconnect ".concat(t.phone,"?"),[{key:"disconnect",label:"Disconnect",color:"danger",actionType:"disconnect"},{key:"cancel",label:"Cancel",color:"default",actionType:"default"}],t)}})}),V=(0,o.Pi)(e=>{let{account:t,onboarding:n}=e,o=(0,a.gM)(),l=e=>t.privileges.indexOf(e)>=0;return(0,s.jsxs)(f.Pd.Provider,{value:{size:"19px"},children:[l("login")?(0,s.jsx)(j,{content:"Retrieve auth code",icon:x.dgU,disabled:!t.lastCode||n,onClick:()=>{var e;o.modals.setMessageBasic("Auth code","As of ".concat((e=t.lastCode.date,function(e){for(let{unit:t,seconds:n}of v)if(e>=n){let s=Math.floor(e/n);return"".concat(s," ").concat(t).concat(1!==s?"s":"")}return"0 seconds"}(Math.floor(Date.now()/1e3)-e))," ago the login code is: ").concat(t.lastCode.value))}}):null,l("manage_connection_state")?(0,s.jsx)(A,{onboarding:n,account:t}):null,l("edit_two_factor_password")?(0,s.jsx)(j,{content:"Edit account's 2FA password",icon:y.U$P,disabled:n,onClick:()=>{o.modals.setEditPasswordClient(t)}}):null,l("remove_account")?(0,s.jsx)(j,{content:"Remove account from Telescope",icon:y.FH3,color:"danger",disabled:n,onClick:()=>{o.modals.setDeleteClient(t)}}):null]})}),P=(0,o.Pi)(e=>{var t,n,o;let{account:a}=e;return(0,s.jsxs)("div",{className:"flex flex-col",children:[(0,s.jsx)("p",{className:"text-bold text-sm",children:null!==(n=null!==(t=a.username)&&void 0!==t?t:a.name)&&void 0!==n?n:"<no username>"}),(0,s.jsx)("p",{className:"text-bold text-sm text-default-400",children:11===(o=a.phone).length?"+".concat(o[0],"-").concat(o.slice(1,4),"-").concat(o.slice(4,7),"-").concat(o.slice(7)):10===o.length?"".concat(o.slice(0,3),"-").concat(o.slice(3,6),"-").concat(o.slice(6)):7===o.length?"".concat(o.slice(0,3),"-").concat(o.slice(3)):o}),10===a.phone.length&&(0,s.jsxs)("p",{className:"text-bold text-sm text-default-400",children:["Code: ",a.phone[5].repeat(5)]}),(0,s.jsx)("p",{className:"text-bold text-sm text-default-400",children:a.email}),(0,s.jsx)("p",{className:"text-bold text-sm text-default-400",children:a.comment})]})}),w=(0,o.Pi)(e=>{let{account:t}=e,n=h(t);return(0,s.jsx)(l.z,{className:"capitalize",color:n,size:"sm",variant:"flat",children:t.status.stage})}),E=(0,o.Pi)(e=>{let{account:t}=e,n=(0,a.gM)(),o=h(t);return null!==t.status.error?(0,s.jsx)("p",{children:t.status.error}):"success"===o||!t.status.inputRequired||0>t.privileges.indexOf("manage_connection_state")?null:(0,s.jsx)(g.A,{isLoading:"warning"===o,onClick:()=>{n.modals.setProvideClient(t)},children:"Provide"})}),N=(0,o.Pi)(e=>{let{account:t,onboarding:n}=e;return(0,s.jsx)("div",{className:"relative flex items-center gap-2",children:(0,s.jsx)(V,{account:t,onboarding:n})})}),S=[{name:"NAME",uid:"name"},{name:"STATUS",uid:"status"},{name:"AUTHENTICATION",uid:"authentication"},{name:"ACTIONS",uid:"actions"}];var R=(0,o.Pi)(e=>{let{onboarding:t}=e,n=(0,a.gM)();return(0,s.jsxs)(c.b,{"aria-label":"Telegram account table",children:[(0,s.jsx)(r.J,{columns:S,children:e=>(0,s.jsx)(i.j,{align:"actions"===e.uid?"center":"start",children:e.name},e.uid)}),(0,s.jsx)(d.y,{items:n.clients,children:n.clients.map(e=>(0,s.jsxs)(u.g,{children:[(0,s.jsx)(m.X,{children:(0,s.jsx)(P,{account:e})}),(0,s.jsx)(m.X,{children:(0,s.jsx)(w,{account:e})}),(0,s.jsx)(m.X,{children:(0,s.jsx)(E,{account:e})}),(0,s.jsx)(m.X,{children:(0,s.jsx)(N,{onboarding:t,account:e})})]},e.phone))})]})})},4531:function(e,t,n){n.d(t,{t:function(){return g}});var s=n(7437),o=n(5430),a=n(5691),l=n(7240),c=n(2265),r=n(5286),i=n(9991),d=n(1094),u=n(3376),m=n(4466);function h(e){return e&&e.length>0?e:null}let g=(0,o.Pi)(()=>{let e=(0,a.gM)(),[t,n]=(0,c.useState)(!1),[o,g]=(0,c.useState)(""),[f,p]=(0,c.useState)(""),[v,x]=(0,c.useState)("");(0,c.useEffect)(()=>{"onboarding"===e.modals.addAccount&&p((0,m.J)()||"")},[e.modals.addAccount]);let b=()=>{e.modals.setAddAccount(null)};return(0,s.jsx)(l.Z,{isOpen:null!==e.modals.addAccount,onClose:b,header:"Add Telegram Account",body:t?(0,s.jsx)(s.Fragment,{children:"Submitting..."}):(0,s.jsxs)("div",{className:"flex flex-col gap-6",children:[(0,s.jsx)(r.Y,{isRequired:!0,type:"text",label:"Phone number",placeholder:"Enter phone number...",labelPlacement:"outside",maxLength:11,pattern:"d{11}",value:o,onValueChange:e=>{g(e)}}),(0,s.jsx)(r.Y,{isRequired:!1,type:"email",isReadOnly:"onboarding"===e.modals.addAccount,label:"E-mail",placeholder:"Enter email...",labelPlacement:"outside",maxLength:255,value:f,onValueChange:e=>{p(e)}}),(0,s.jsx)(r.Y,{isRequired:!1,type:"text",label:"Comment",placeholder:"Account belongs to...",labelPlacement:"outside",maxLength:300,value:v,onValueChange:e=>{x(e)}})]}),footer:t?(0,s.jsx)(i.c,{}):(0,s.jsxs)(s.Fragment,{children:[(0,s.jsx)(d.A,{color:"danger",variant:"light",onPress:b,children:"Close"}),(0,s.jsx)(d.A,{color:"primary",onPress:async()=>{n(!0);let t=await u.s.getInstance().addAccount(o,h(f),h(v));t.success?"onboarding"===e.modals.addAccount&&e.modals.setAddAccountPhone(o):e.modals.setMessageBasic("Error","Failed to add account: ".concat(t.error)),e.modals.setAddAccount(null),n(!1)},children:"Submit"})]})})})},4992:function(e,t,n){n.d(t,{E:function(){return d}});var s=n(7437),o=n(5430),a=n(7240),l=n(5691),c=n(1094);n(2265);var r=n(3376);let i={default:e=>{e.modals.clearMessage()},disconnect:e=>{var t;let n=null===(t=e.modals.message)||void 0===t?void 0:t.client;e.modals.clearMessage(),n&&r.s.getInstance().disconnectClient(n.phone).then(t=>{t.success?e.modals.setMessageBasic("Success","Disconnected account ".concat(n.phone,".")):e.modals.setMessageBasic("Error","Couldn't disconnect account ".concat(n.phone,": ").concat(t.error))})},add_test_account:e=>{e.modals.clearMessage(),r.s.getInstance().addTestAccount().then(t=>{t.success?e.modals.setMessageBasic("Success","Created test account."):e.modals.setMessageBasic("Error","Couldn't create test account: ".concat(t.error))})}},d=(0,o.Pi)(()=>{var e,t,n;let o=(0,l.gM)(),r=o.modals;return(0,s.jsx)(a.Z,{isOpen:null!==r.message,onClose:()=>{r.clearMessage()},header:null===(e=r.message)||void 0===e?void 0:e.title,body:(0,s.jsx)("p",{children:null===(t=r.message)||void 0===t?void 0:t.message}),footer:null===(n=r.message)||void 0===n?void 0:n.buttons.map(e=>(0,s.jsx)(c.A,{color:e.color||void 0,onPress:()=>{i[e.actionType](o)},children:e.label},e.key))})})},7240:function(e,t,n){var s=n(7437),o=n(1496),a=n(9960),l=n(5256),c=n(1887),r=n(7971);n(2265);let i=(0,n(5430).Pi)(e=>(0,s.jsx)(o.R,{isOpen:e.isOpen,onClose:e.onClose,children:(0,s.jsxs)(a.A,{children:[(0,s.jsx)(l.k,{className:"flex flex-col gap-1",children:e.header}),(0,s.jsx)(c.I,{children:e.body}),(0,s.jsx)(r.R,{children:e.footer})]})}));t.Z=i},5735:function(e,t,n){n.d(t,{v:function(){return h}});var s=n(7437),o=n(5430),a=n(5691),l=n(7240),c=n(2265),r=n(9991),i=n(1094),d=n(5286),u=n(3376);let m={PasswordRequired:{name:"PasswordRequired",inputType:"text",label:"Password",placeholder:"Enter the account password",filter_regex:/\s/g,validate:e=>e.length>0?null:"Cannot be empty."},AuthCodeRequired:{name:"AuthCodeRequired",inputType:"text",label:"Auth Code",placeholder:"Enter the Telegram auth code",maxLength:5,filter_regex:/\D/g,validate:e=>/^[0-9]{5}$/.test(e)?null:"Auth code is exactly 5 digits."},EmailCodeRequired:{name:"EmailCodeRequired",inputType:"text",label:"E-mail code",placeholder:"Enter code from email",filter_regex:/\s/g,validate:e=>e.length>0?null:"Must enter an email code."}},h=(0,o.Pi)(()=>{var e;let t=(0,a.gM)(),[n,o]=(0,c.useState)(!1),[h,g]=(0,c.useState)(""),f=null!==t.modals.provide,p=f?m[t.modals.provide.status.stage]:null,v=null;null!==p&&(null==p?void 0:p.validate)!==null&&(v=p.validate(h));let x=()=>{t.modals.setProvideClient(null),g("")};return(0,s.jsx)(l.Z,{isOpen:f,onClose:x,header:null===(e=t.modals.provide)||void 0===e?void 0:e.status.stage,body:n?(0,s.jsx)(s.Fragment,{children:"Submitting..."}):(0,s.jsxs)(s.Fragment,{children:[(0,s.jsx)("p",{children:"Please enter the thingy."}),(0,s.jsx)("div",{children:(0,s.jsx)(d.Y,{isRequired:!0,type:null==p?void 0:p.inputType,label:null==p?void 0:p.label,placeholder:null==p?void 0:p.placeholder,maxLength:null==p?void 0:p.maxLength,isInvalid:null!==v,color:null!==v?"danger":"success",errorMessage:null!=v?v:"",value:h,onValueChange:e=>{(null==p?void 0:p.filter_regex)?g(e.replaceAll(p.filter_regex,"")):g(e)}})})]}),footer:n?(0,s.jsx)(r.c,{}):(0,s.jsxs)(s.Fragment,{children:[(0,s.jsx)(i.A,{color:"danger",variant:"light",onPress:x,children:"Close"}),(0,s.jsx)(i.A,{color:"primary",onPress:async()=>{try{o(!0);let e=u.s.getInstance(),n=t.modals.provide,s=await e.submitValue(null==n?void 0:n.phone,null==n?void 0:n.status.stage,h);if(await new Promise(e=>setTimeout(e,2e3)),o(!1),s.success){let e=t.clients.find(e=>e.phone===(null==n?void 0:n.phone));e&&e.updateStatus({...e.status,inputRequired:!1})}else console.error("Error submitting code to server: ".concat(s.error))}catch(e){console.error("Error submitting code to server: ",e)}t.modals.setProvideClient(null),g("")},children:"Submit"})]})})})}}]);