"use strict";(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[97],{7484:function(e,t,n){n.d(t,{c:function(){return h},wm:function(){return x},no:function(){return N},gM:function(){return A}});var s,a,o,l,c=n(8890),i=n(2265);let r=c.V5.enumeration("ActionType",["default","disconnect","add_test_account"]),d=c.V5.model({key:c.V5.string,label:c.V5.string,color:c.V5.maybeNull(c.V5.enumeration("Color",["default","primary","secondary","success","warning","danger"])),actionType:r}),u=c.V5.maybeNull(c.V5.reference(c.V5.late(()=>n(7484).c),{get(e,t){var n;return(null===(n=(0,c.yj)(t).clients)||void 0===n?void 0:n.find(t=>t.phone===e))||null},set:e=>e.phone})),m=c.V5.model({title:c.V5.string,message:c.V5.string,buttons:c.V5.array(d),client:u}),g=c.V5.model({addAccount:c.V5.maybeNull(c.V5.enumeration("AddAccountMode",["normal","onboarding"])),addAccountPhone:c.V5.maybeNull(c.V5.string),provide:u,editPassword:u,deleteClient:u,message:c.V5.maybeNull(m)}).actions(e=>({setProvideClient:function(t){e.provide=t},setEditPasswordClient:function(t){e.editPassword=t},setDeleteClient:function(t){e.deleteClient=t},setAddAccount:function(t){e.addAccount=t},setAddAccountPhone:function(t){e.addAccountPhone=t},setMessage:function(t,n,s,a){e.message=m.create({title:t,message:n,buttons:s,client:a||null})},setMessageBasic:function(t,n,s){e.message=m.create({title:t,message:n,buttons:[{key:"okay",label:"Okay",color:"primary",actionType:"default"}],client:s||null})},clearMessage:function(){e.message=null}}));(s=o||(o={})).ADD_ACCOUNT="ADD_ACCOUNT",s.ADD_TEST_ACCOUNT="ADD_TEST_ACCOUNT",s.SUBMIT_VALUE="SUBMIT_VALUE",s.DELETE_ACCOUNT="DELETE_ACCOUNT",s.CONNECT_CLIENT="CONNECT_CLIENT",s.DISCONNECT_CLIENT="DISCONNECT_CLIENT",s.SET_PASSWORD="SET_PASSWORD";let S=c.V5.model({socketState:c.V5.enumeration(["connecting","open","closed","error"]),responseStatus:c.V5.enumeration(["waiting","received"])}).volatile(e=>({socket:null})).actions(e=>({setState(t){e.socketState=t},connect(t){e.socket&&e.socket.close(),this.setState("connecting"),e.socket=new WebSocket(t),e.socket.onopen=()=>{this.setState("open")},e.socket.onclose=()=>{this.setState("closed")},e.socket.onerror=e=>{this.setState("error")},e.socket.onmessage=t=>{let n=JSON.parse(t.data);console.log(n),n.hasOwnProperty("type")?(0,c.yj)(e).updateFromSocket(n):console.error("WebSocket data must contain an `id` field")}},sendMessage(t){e.socket&&e.socket.readyState===WebSocket.OPEN?e.socket.send(JSON.stringify(t)):console.error("Failed to send message: WebSocket is closed")},addAccount(e,t,n){this.sendMessage({type:o.ADD_ACCOUNT,data:{phone:e,email:t,comment:n}})},addTestAccount(){this.sendMessage({type:o.ADD_TEST_ACCOUNT})},submitValue(e,t,n){this.sendMessage({type:o.SUBMIT_VALUE,data:{phone:e,stage:t,value:n}})},deleteAccount(e){this.sendMessage({type:o.DELETE_ACCOUNT,data:{phone:e}})},disconnectClient(e){this.sendMessage({type:o.DISCONNECT_CLIENT,data:{phone:e}})},connectClient(e){this.sendMessage({type:o.CONNECT_CLIENT,data:{phone:e}})},setPassword(e,t){this.sendMessage({type:o.SET_PASSWORD,data:{phone:e,password:t}})},setWaiting(){e.responseStatus="waiting"},setReceived(){e.responseStatus="received"},disconnect(){e.socket&&(e.socket.close(),e.socket=null,e.socketState="closed")}}));(a=l||(l={})).SSO_START="SSO_START",a.CLIENT_START="CLIENT_START",a.ADD_ACCOUNT_RESPONSE="ADD_ACCOUNT_RESPONSE",a.ADD_TEST_ACCOUNT_RESPONSE="ADD_TEST_ACCOUNT_RESPONSE",a.SUBMIT_VALUE_RESPONSE="SUBMIT_VALUE_RESPONSE",a.DELETE_ACCOUNT_RESPONSE="DELETE_ACCOUNT_RESPONSE",a.CONNECT_CLIENT_RESPONSE="CONNECT_CLIENT_RESPONSE",a.DISCONNECT_CLIENT_RESPONSE="DISCONNECT_CLIENT_RESPONSE",a.SET_PASSWORD_RESPONSE="SET_PASSWORD_RESPONSE";let E=c.V5.model({stage:c.V5.enumeration("AuthState",["ClientNotStarted","WaitingOnServer","PasswordRequired","AuthCodeRequired","EmailRequired","EmailCodeRequired","AuthorizationSuccess","ConnectionClosed","ErrorOccurred","PhoneNumberRequired","RegistrationRequired"]),inputRequired:c.V5.boolean,error:c.V5.maybeNull(c.V5.string)}),C=c.V5.enumeration("Privileges",["view","edit_two_factor_password","login","manage_connection_state","remove_account"]),h=c.V5.model({name:c.V5.maybeNull(c.V5.string),username:c.V5.maybeNull(c.V5.string),email:c.V5.maybeNull(c.V5.string),comment:c.V5.maybeNull(c.V5.string),phone:c.V5.string,lastCode:c.V5.maybeNull(c.V5.model({value:c.V5.number,date:c.V5.number})),status:E,privileges:c.V5.array(C)}).actions(e=>({updateStatus(t){e.status=E.create(t)}})),p=c.V5.enumeration("Environment",["Staging","Production"]),N=c.V5.model({clients:c.V5.array(h),ssoClient:u,ssoEmail:c.V5.maybeNull(c.V5.string),clientsState:c.V5.enumeration("State",["pending","done"]),environment:p,modals:g,socket:S}).actions(e=>({updateFromSocket:function(t){switch(console.log(t.type),t.type){case l.CLIENT_START:e.clients=t.data.items||[],e.environment=t.data.environment,e.clientsState="done";break;case l.SSO_START:e.ssoEmail=t.data.email,e.ssoClient=e.clients.find(t=>t.email===e.ssoEmail);break;case l.ADD_ACCOUNT_RESPONSE:e.socket.responseStatus="received","ERROR"===t.data.status&&e.modals.setMessageBasic("Error","Failed to add account: ".concat(t.data.error));break;case l.ADD_TEST_ACCOUNT_RESPONSE:e.socket.responseStatus="received","ERROR"===t.data.status?e.modals.setMessageBasic("Error","Couldn't create test account: ".concat(t.data.error)):e.modals.setMessageBasic("Success","Created test account.");break;case l.SUBMIT_VALUE_RESPONSE:e.socket.responseStatus="received","ERROR"===t.data.status&&console.error("SUBMIT_VALUE_RESPONSE: ".concat(t.data.error));break;case l.DELETE_ACCOUNT_RESPONSE:e.modals.setDeleteClient(null),e.socket.responseStatus="received","ERROR"===t.data.status&&e.modals.setMessageBasic("Error","Failed to delete account: ".concat(t.data.error));break;case l.CONNECT_CLIENT_RESPONSE:e.socket.responseStatus="received","ERROR"===t.data.status?e.modals.setMessageBasic("Error","Couldn't connect account: ".concat(t.data.error)):e.modals.setMessageBasic("Success","Connected account.");break;case l.DISCONNECT_CLIENT_RESPONSE:e.socket.responseStatus="received","ERROR"===t.data.status?e.modals.setMessageBasic("Error","Couldn't disconnect account: ".concat(t.data.error)):e.modals.setMessageBasic("Success","Disconnected account.");break;case l.SET_PASSWORD_RESPONSE:e.socket.responseStatus="received","ERROR"===t.data.status&&e.modals.setMessageBasic("Error","Failed to edit account password for: ".concat(t.data.error))}}})).create({clients:[],clientsState:"pending",environment:"Production",modals:{},socket:{socketState:"connecting",responseStatus:"received"}}),T=(0,i.createContext)(null),x=T.Provider;function A(){let e=(0,i.useContext)(T);if(null===e)throw Error("Store cannot be null, please add a context provider");return e}(0,c.cf)(N,e=>{console.log("snapshot",e)})},6283:function(e,t,n){n.d(t,{wQ:function(){return O},QB:function(){return v},gE:function(){return b},ZP:function(){return P}});var s=n(7437),a=n(5430),o=n(7484),l=n(9386),c=n(7265),i=n(9629),r=n(9139),d=n(964),u=n(3908),m=n(1272);function g(e){let t="warning";return"AuthorizationSuccess"===e.status.stage?t="success":"ClientNotStarted"===e.status.stage?t="default":("ConnectionClosed"===e.status.stage||"ErrorOccurred"===e.status.stage||!0===e.status.inputRequired)&&(t="danger"),t}n(2265);var S=n(4794),E=n(1810),C=n(8941);let h=[{unit:"year",seconds:31104e3},{unit:"month",seconds:2592e3},{unit:"day",seconds:86400},{unit:"hour",seconds:3600},{unit:"minute",seconds:60},{unit:"second",seconds:1}];var p=n(4983),N=n(6356),T=n(9726);function x(e){return(0,s.jsx)(C.e,{content:e.content,children:(0,s.jsx)(S.A,{isIconOnly:!0,color:e.color||"default","aria-label":e.arialabel||e.content,onClick:e.onClick,isDisabled:e.disabled,children:(0,s.jsx)(e.icon,{className:e.iconClass})})})}let A=(0,a.Pi)(e=>{let{account:t,onboarding:n}=e,a=(0,o.gM)();return"ClientNotStarted"===t.status.stage?(0,s.jsx)(x,{content:"Connect Telegram session for this account",icon:N.y6x,disabled:n,onClick:()=>{a.socket.connectClient(t.phone)}}):(0,s.jsx)(x,{content:"Disconnect currently active Telegram session",icon:T.ZUl,iconClass:"font-bold",disabled:n,onClick:()=>{a.modals.setMessage("Disconnect","Really disconnect ".concat(t.phone,"?"),[{key:"disconnect",label:"Disconnect",color:"danger",actionType:"disconnect"},{key:"cancel",label:"Cancel",color:"default",actionType:"default"}],t)}})}),_=(0,a.Pi)(e=>{let{account:t,onboarding:n}=e,a=(0,o.gM)(),l=e=>t.privileges.indexOf(e)>=0;return(0,s.jsxs)(E.Pd.Provider,{value:{size:"19px"},children:[l("login")?(0,s.jsx)(x,{content:"Retrieve auth code",icon:p.dgU,disabled:!t.lastCode||n,onClick:()=>{var e;a.modals.setMessageBasic("Auth code","As of ".concat((e=t.lastCode.date,function(e){for(let{unit:t,seconds:n}of h)if(e>=n){let s=Math.floor(e/n);return"".concat(s," ").concat(t).concat(1!==s?"s":"")}return"0 seconds"}(Math.floor(Date.now()/1e3)-e))," ago the login code is: ").concat(t.lastCode.value))}}):null,l("manage_connection_state")?(0,s.jsx)(A,{onboarding:n,account:t}):null,l("edit_two_factor_password")?(0,s.jsx)(x,{content:"Edit account's 2FA password",icon:N.U$P,disabled:n,onClick:()=>{a.modals.setEditPasswordClient(t)}}):null,l("remove_account")?(0,s.jsx)(x,{content:"Remove account from Telescope",icon:N.FH3,color:"danger",disabled:n,onClick:()=>{a.modals.setDeleteClient(t)}}):null]})}),v=(0,a.Pi)(e=>{var t,n,a;let{account:o}=e;return(0,s.jsxs)("div",{className:"flex flex-col",children:[(0,s.jsx)("p",{className:"text-bold text-sm",children:null!==(n=null!==(t=o.username)&&void 0!==t?t:o.name)&&void 0!==n?n:"<no username>"}),(0,s.jsx)("p",{className:"text-bold text-sm text-default-400",children:11===(a=o.phone).length?"+".concat(a[0],"-").concat(a.slice(1,4),"-").concat(a.slice(4,7),"-").concat(a.slice(7)):10===a.length?"".concat(a.slice(0,3),"-").concat(a.slice(3,6),"-").concat(a.slice(6)):7===a.length?"".concat(a.slice(0,3),"-").concat(a.slice(3)):a}),10===o.phone.length&&(0,s.jsxs)("p",{className:"text-bold text-sm text-default-400",children:["Code: ",o.phone[5].repeat(5)]}),(0,s.jsx)("p",{className:"text-bold text-sm text-default-400",children:o.email}),(0,s.jsx)("p",{className:"text-bold text-sm text-default-400",children:o.comment})]})}),b=(0,a.Pi)(e=>{let{account:t}=e,n=g(t);return(0,s.jsx)(l.z,{className:"capitalize",color:n,size:"sm",variant:"flat",children:t.status.stage})}),O=(0,a.Pi)(e=>{let{account:t}=e,n=(0,o.gM)(),a=g(t);return null!==t.status.error?(0,s.jsx)("p",{children:t.status.error}):"success"===a||!t.status.inputRequired||0>t.privileges.indexOf("manage_connection_state")?null:(0,s.jsx)(S.A,{isLoading:"warning"===a,onClick:()=>{n.modals.setProvideClient(t)},children:"Provide"})}),f=(0,a.Pi)(e=>{let{account:t,onboarding:n}=e;return(0,s.jsx)("div",{className:"relative flex items-center gap-2",children:(0,s.jsx)(_,{account:t,onboarding:n})})}),R=[{name:"NAME",uid:"name"},{name:"STATUS",uid:"status"},{name:"AUTHENTICATION",uid:"authentication"},{name:"ACTIONS",uid:"actions"}];var P=(0,a.Pi)(e=>{let{onboarding:t}=e,n=(0,o.gM)();return(0,s.jsxs)(c.b,{"aria-label":"Telegram account table",children:[(0,s.jsx)(i.J,{columns:R,children:e=>(0,s.jsx)(r.j,{align:"actions"===e.uid?"center":"start",children:e.name},e.uid)}),(0,s.jsx)(d.y,{items:n.clients,children:n.clients.map(e=>(0,s.jsxs)(u.g,{children:[(0,s.jsx)(m.X,{children:(0,s.jsx)(v,{account:e})}),(0,s.jsx)(m.X,{children:(0,s.jsx)(b,{account:e})}),(0,s.jsx)(m.X,{children:(0,s.jsx)(O,{account:e})}),(0,s.jsx)(m.X,{children:(0,s.jsx)(f,{onboarding:t,account:e})})]},e.phone))})]})})},4531:function(e,t,n){n.d(t,{t:function(){return m}});var s=n(7437),a=n(5430),o=n(7484),l=n(7240),c=n(2265),i=n(5286),r=n(9991),d=n(1094);function u(e){return e&&e.length>0?e:null}let m=(0,a.Pi)(()=>{let e=(0,o.gM)(),[t,n]=(0,c.useState)(!1),[a,m]=(0,c.useState)(""),[g,S]=(0,c.useState)(""),[E,C]=(0,c.useState)("");(0,c.useEffect)(()=>{"onboarding"===e.modals.addAccount&&S(e.ssoEmail||"")},[e.modals.addAccount]);let h=()=>{e.modals.setAddAccount(null)};return(0,s.jsx)(l.Z,{isOpen:null!==e.modals.addAccount,onClose:h,header:"Add Telegram Account",body:t?(0,s.jsx)(s.Fragment,{children:"Submitting..."}):(0,s.jsxs)("div",{className:"flex flex-col gap-6",children:[(0,s.jsx)(i.Y,{isRequired:!0,type:"text",label:"Phone number",placeholder:"Enter phone number...",labelPlacement:"outside",maxLength:11,pattern:"d{11}",value:a,onValueChange:e=>{m(e)}}),(0,s.jsx)(i.Y,{isRequired:!1,type:"email",isReadOnly:"onboarding"===e.modals.addAccount,label:"E-mail",placeholder:"Enter email...",labelPlacement:"outside",maxLength:255,value:g,onValueChange:e=>{S(e)}}),(0,s.jsx)(i.Y,{isRequired:!1,type:"text",label:"Comment",placeholder:"Account belongs to...",labelPlacement:"outside",maxLength:300,value:E,onValueChange:e=>{C(e)}})]}),footer:t?(0,s.jsx)(r.c,{}):(0,s.jsxs)(s.Fragment,{children:[(0,s.jsx)(d.A,{color:"danger",variant:"light",onPress:h,children:"Close"}),(0,s.jsx)(d.A,{color:"primary",onPress:async()=>{n(!0),e.socket.addAccount(a,u(g),u(E)),"onboarding"===e.modals.addAccount&&e.modals.setAddAccountPhone(a),e.modals.setAddAccount(null),n(!1)},children:"Submit"})]})})})},4992:function(e,t,n){n.d(t,{E:function(){return r}});var s=n(7437),a=n(5430),o=n(7240),l=n(7484),c=n(1094);n(2265);let i={default:e=>{e.modals.clearMessage()},disconnect:e=>{var t;let n=null===(t=e.modals.message)||void 0===t?void 0:t.client;e.modals.clearMessage(),n&&e.socket.disconnectClient(n.phone)},add_test_account:e=>{e.modals.clearMessage(),e.socket.addTestAccount()}},r=(0,a.Pi)(()=>{var e,t,n;let a=(0,l.gM)(),r=a.modals;return(0,s.jsx)(o.Z,{isOpen:null!==r.message,onClose:()=>{r.clearMessage()},header:null===(e=r.message)||void 0===e?void 0:e.title,body:(0,s.jsx)("p",{children:null===(t=r.message)||void 0===t?void 0:t.message}),footer:null===(n=r.message)||void 0===n?void 0:n.buttons.map(e=>(0,s.jsx)(c.A,{color:e.color||void 0,onPress:()=>{i[e.actionType](a)},children:e.label},e.key))})})},7240:function(e,t,n){var s=n(7437),a=n(1496),o=n(9960),l=n(5256),c=n(1025),i=n(7971);n(2265);let r=(0,n(5430).Pi)(e=>(0,s.jsx)(a.R,{isOpen:e.isOpen,onClose:e.onClose,children:(0,s.jsxs)(o.A,{children:[(0,s.jsx)(l.k,{className:"flex flex-col gap-1",children:e.header}),(0,s.jsx)(c.I,{children:e.body}),(0,s.jsx)(i.R,{children:e.footer})]})}));t.Z=r},5735:function(e,t,n){n.d(t,{v:function(){return m}});var s=n(7437),a=n(5430),o=n(7484),l=n(7240),c=n(2265),i=n(9991),r=n(1094),d=n(5286);let u={PasswordRequired:{name:"PasswordRequired",inputType:"text",label:"Password",placeholder:"Enter the account password",filter_regex:/\s/g,validate:e=>e.length>0?null:"Cannot be empty."},AuthCodeRequired:{name:"AuthCodeRequired",inputType:"text",label:"Auth Code",placeholder:"Enter the Telegram auth code",maxLength:5,filter_regex:/\D/g,validate:e=>/^[0-9]{5}$/.test(e)?null:"Auth code is exactly 5 digits."},EmailCodeRequired:{name:"EmailCodeRequired",inputType:"text",label:"E-mail code",placeholder:"Enter code from email",filter_regex:/\s/g,validate:e=>e.length>0?null:"Must enter an email code."}},m=(0,a.Pi)(()=>{var e;let t=(0,o.gM)(),[n,a]=(0,c.useState)(!1),[m,g]=(0,c.useState)(""),S=null!==t.modals.provide,E=S?u[t.modals.provide.status.stage]:null,C=null;null!==E&&(null==E?void 0:E.validate)!==null&&(C=E.validate(m));let h=()=>{t.modals.setProvideClient(null),g("")};return(0,s.jsx)(l.Z,{isOpen:S,onClose:h,header:null===(e=t.modals.provide)||void 0===e?void 0:e.status.stage,body:n?(0,s.jsx)(s.Fragment,{children:"Submitting..."}):(0,s.jsxs)(s.Fragment,{children:[(0,s.jsx)("p",{children:"Please enter the thingy."}),(0,s.jsx)("div",{children:(0,s.jsx)(d.Y,{isRequired:!0,type:null==E?void 0:E.inputType,label:null==E?void 0:E.label,placeholder:null==E?void 0:E.placeholder,maxLength:null==E?void 0:E.maxLength,isInvalid:null!==C,color:null!==C?"danger":"success",errorMessage:null!=C?C:"",value:m,onValueChange:e=>{(null==E?void 0:E.filter_regex)?g(e.replaceAll(E.filter_regex,"")):g(e)}})})]}),footer:n?(0,s.jsx)(i.c,{}):(0,s.jsxs)(s.Fragment,{children:[(0,s.jsx)(r.A,{color:"danger",variant:"light",onPress:h,children:"Close"}),(0,s.jsx)(r.A,{color:"primary",onPress:async()=>{a(!0);let e=t.modals.provide;t.socket.submitValue(null==e?void 0:e.phone,null==e?void 0:e.status.stage,m),a(!1),t.modals.setProvideClient(null),g("")},children:"Submit"})]})})})}}]);