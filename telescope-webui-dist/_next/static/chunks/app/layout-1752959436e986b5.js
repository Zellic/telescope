(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[185],{31:function(e,t,s){Promise.resolve().then(s.bind(s,8941)),Promise.resolve().then(s.bind(s,4384)),Promise.resolve().then(s.bind(s,1410)),Promise.resolve().then(s.bind(s,5137)),Promise.resolve().then(s.t.bind(s,231,23)),Promise.resolve().then(s.t.bind(s,4332,23)),Promise.resolve().then(s.t.bind(s,2882,23)),Promise.resolve().then(s.t.bind(s,6571,23))},8941:function(e,t,s){"use strict";s.d(t,{Providers:function(){return d}});var a=s(7437);s(2265);var o=s(4140),n=s(6463),r=s(5169),i=s(7484);let c=e=>{let{children:t}=e;return(0,a.jsx)(i.wm,{value:i.no,children:t})};function d(e){let{children:t,themeProps:s}=e,i=(0,n.useRouter)();return(0,a.jsx)(o.w,{navigate:i.push,children:(0,a.jsx)(r.f,{...s,children:(0,a.jsx)(c,{children:t})})})}},7484:function(e,t,s){"use strict";s.d(t,{c:function(){return O},wm:function(){return g},no:function(){return R},gM:function(){return A}});var a,o,n,r,i=s(8890),c=s(2265);let d=i.V5.enumeration("ActionType",["default","disconnect","add_test_account","terminate"]),l=i.V5.model({key:i.V5.string,label:i.V5.string,color:i.V5.maybeNull(i.V5.enumeration("Color",["default","primary","secondary","success","warning","danger"])),actionType:d}),S=i.V5.maybeNull(i.V5.reference(i.V5.late(()=>s(7484).c),{get(e,t){var s;return(null===(s=(0,i.yj)(t).clients)||void 0===s?void 0:s.find(t=>t.phone===e))||null},set:e=>e.phone})),E=i.V5.model({title:i.V5.string,message:i.V5.string,buttons:i.V5.array(l),client:S}),u=i.V5.model({addAccount:i.V5.maybeNull(i.V5.enumeration("AddAccountMode",["normal","onboarding"])),provide:S,editPassword:S,viewPassword:S,viewPasswordState:i.V5.enumeration("GetPassword",["failure","ok","waiting"]),viewPasswordPass:i.V5.string,deleteClient:S,message:i.V5.maybeNull(E)}).actions(e=>({setProvideClient:function(t){e.provide=t},setEditPasswordClient:function(t){e.editPassword=t},setViewPasswordClient:function(t){e.viewPassword=t},setViewPassword:function(t){e.viewPasswordPass=t},setViewPasswordState:function(t){e.viewPasswordState=t},setDeleteClient:function(t){e.deleteClient=t},setAddAccount:function(t){e.addAccount=t},setMessage:function(t,s,a,o){e.message=E.create({title:t,message:s,buttons:a,client:o||null})},setMessageBasic:function(t,s,a){e.message=E.create({title:t,message:s,buttons:[{key:"okay",label:"Okay",color:"primary",actionType:"default"}],client:a||null})},clearMessage:function(){e.message=null}}));(a=n||(n={})).ADD_ACCOUNT="ADD_ACCOUNT",a.ADD_TEST_ACCOUNT="ADD_TEST_ACCOUNT",a.SUBMIT_VALUE="SUBMIT_VALUE",a.DELETE_ACCOUNT="DELETE_ACCOUNT",a.CONNECT_CLIENT="CONNECT_CLIENT",a.DISCONNECT_CLIENT="DISCONNECT_CLIENT",a.SET_PASSWORD="SET_PASSWORD",a.GET_PASSWORD="GET_PASSWORD",a.TERMINATE_OTHER_SESSIONS="TERMINATE_OTHER_SESSIONS";let _=i.V5.model({socketState:i.V5.enumeration(["connecting","open","closed","error"]),responseStatus:i.V5.enumeration(["waiting","received"])}).volatile(e=>({socket:null})).actions(e=>({setState(t){e.socketState=t},connect(t){e.socket&&e.socket.close(),this.setState("connecting"),e.socket=new WebSocket(t),e.socket.onopen=()=>{this.setState("open")},e.socket.onclose=()=>{this.setState("closed")},e.socket.onerror=e=>{this.setState("error")},e.socket.onmessage=t=>{let s=JSON.parse(t.data);s.hasOwnProperty("type")?(0,i.yj)(e).updateFromSocket(s):console.error("WebSocket data must contain an `id` field")}},sendMessage(t){e.socket&&e.socket.readyState===WebSocket.OPEN?e.socket.send(JSON.stringify(t)):console.error("Failed to send message: WebSocket is closed")},addAccount(e,t,s){this.sendMessage({type:n.ADD_ACCOUNT,data:{phone:e,email:t,comment:s}})},addTestAccount(){this.sendMessage({type:n.ADD_TEST_ACCOUNT})},submitValue(e,t,s){this.sendMessage({type:n.SUBMIT_VALUE,data:{phone:e,stage:t,value:s}})},deleteAccount(e){this.sendMessage({type:n.DELETE_ACCOUNT,data:{phone:e}})},disconnectClient(e){this.sendMessage({type:n.DISCONNECT_CLIENT,data:{phone:e}})},terminateOtherSessions(e){this.sendMessage({type:n.TERMINATE_OTHER_SESSIONS,data:{phone:e}})},connectClient(e){this.sendMessage({type:n.CONNECT_CLIENT,data:{phone:e}})},setPassword(e,t){this.sendMessage({type:n.SET_PASSWORD,data:{phone:e,password:t}})},getPassword(t){(0,i.yj)(e).modals.setViewPasswordState("waiting"),this.sendMessage({type:n.GET_PASSWORD,data:{phone:t}})},setWaiting(){e.responseStatus="waiting"},setReceived(){e.responseStatus="received"},disconnect(){e.socket&&(e.socket.close(),e.socket=null,e.socketState="closed")}}));(o=r||(r={})).SSO_START="SSO_START",o.CLIENT_START="CLIENT_START",o.ADD_ACCOUNT_RESPONSE="ADD_ACCOUNT_RESPONSE",o.ADD_TEST_ACCOUNT_RESPONSE="ADD_TEST_ACCOUNT_RESPONSE",o.SUBMIT_VALUE_RESPONSE="SUBMIT_VALUE_RESPONSE",o.DELETE_ACCOUNT_RESPONSE="DELETE_ACCOUNT_RESPONSE",o.CONNECT_CLIENT_RESPONSE="CONNECT_CLIENT_RESPONSE",o.DISCONNECT_CLIENT_RESPONSE="DISCONNECT_CLIENT_RESPONSE",o.SET_PASSWORD_RESPONSE="SET_PASSWORD_RESPONSE",o.GET_PASSWORD_RESPONSE="GET_PASSWORD_RESPONSE",o.TERMINATE_OTHER_SESSIONS_RESPONSE="TERMINATE_OTHER_SESSIONS_RESPONSE";var N=s(357);let T=i.V5.model({stage:i.V5.enumeration("AuthState",["ClientNotStarted","WaitingOnServer","PasswordRequired","AuthCodeRequired","EmailRequired","EmailCodeRequired","AuthorizationSuccess","ConnectionClosed","ErrorOccurred","PhoneNumberRequired","RegistrationRequired"]),inputRequired:i.V5.boolean,error:i.V5.maybeNull(i.V5.string)}),C=i.V5.enumeration("Privileges",["view","edit_two_factor_password","login","manage_connection_state","remove_account"]),O=i.V5.model({name:i.V5.maybeNull(i.V5.string),username:i.V5.maybeNull(i.V5.string),email:i.V5.maybeNull(i.V5.string),comment:i.V5.maybeNull(i.V5.string),phone:i.V5.string,two_factor_pass_is_set:i.V5.boolean,two_factor_protected:i.V5.maybeNull(i.V5.boolean),lastCode:i.V5.maybeNull(i.V5.model({value:i.V5.number,date:i.V5.number})),status:T,privileges:i.V5.array(C)}).actions(e=>({updateStatus(t){e.status=T.create(t)}})),m=i.V5.enumeration("Environment",["Development","Production"]),R=i.V5.model({clients:i.V5.array(O),ssoClient:S,ssoEmail:i.V5.maybeNull(i.V5.string),clientsState:i.V5.enumeration("State",["pending","done"]),environment:m,modals:u,socket:_}).actions(e=>({updateFromSocket:function(t){switch(N.env.NEXT_PUBLIC_DEBUG_LOG&&console.log(t),t.type){case r.CLIENT_START:e.clients=t.data.items||[],e.environment=t.data.environment,e.clientsState="done",e.ssoEmail&&(e.ssoClient=e.clients.find(t=>t.email===e.ssoEmail));break;case r.SSO_START:e.ssoEmail=t.data.email,e.ssoClient=e.clients.find(t=>t.email===e.ssoEmail);break;case r.ADD_ACCOUNT_RESPONSE:e.socket.responseStatus="received","ERROR"===t.data.status&&e.modals.setMessageBasic("Error","Failed to add account: ".concat(t.data.error));break;case r.ADD_TEST_ACCOUNT_RESPONSE:e.socket.responseStatus="received","ERROR"===t.data.status?e.modals.setMessageBasic("Error","Couldn't create test account: ".concat(t.data.error)):e.modals.setMessageBasic("Success","Created test account.");break;case r.SUBMIT_VALUE_RESPONSE:e.socket.responseStatus="received","ERROR"===t.data.status&&console.error("SUBMIT_VALUE_RESPONSE: ".concat(t.data.error));break;case r.DELETE_ACCOUNT_RESPONSE:e.modals.setDeleteClient(null),e.socket.responseStatus="received","ERROR"===t.data.status&&e.modals.setMessageBasic("Error","Failed to delete account: ".concat(t.data.error));break;case r.CONNECT_CLIENT_RESPONSE:e.socket.responseStatus="received","ERROR"===t.data.status?e.modals.setMessageBasic("Error","Couldn't connect account: ".concat(t.data.error)):e.modals.setMessageBasic("Success","Connected account.");break;case r.DISCONNECT_CLIENT_RESPONSE:e.socket.responseStatus="received","ERROR"===t.data.status?e.modals.setMessageBasic("Error","Couldn't disconnect account: ".concat(t.data.error)):e.modals.setMessageBasic("Success","Disconnected account.");break;case r.SET_PASSWORD_RESPONSE:e.socket.responseStatus="received","ERROR"===t.data.status&&e.modals.setMessageBasic("Error","Failed to edit account password for: ".concat(t.data.error));break;case r.GET_PASSWORD_RESPONSE:e.socket.responseStatus="received","ERROR"===t.data.status?(e.modals.setViewPasswordState("failure"),e.modals.setMessageBasic("Error","".concat(t.data.error))):(e.modals.setViewPassword(t.data.value),e.modals.setViewPasswordState("ok"));break;case r.TERMINATE_OTHER_SESSIONS_RESPONSE:e.socket.responseStatus="received","ERROR"===t.data.status?e.modals.setMessageBasic("Error","Couldn't terminate other sessions: ".concat(t.data.error)):e.modals.setMessageBasic("Success","Terminated all other sessions.")}},setMockStage:function(t){e.ssoClient&&(e.ssoClient.status.stage=t)}})).create({clients:[],clientsState:"pending",environment:"Production",modals:{viewPasswordPass:"",viewPasswordState:"waiting"},socket:{socketState:"connecting",responseStatus:"received"}}),P=(0,c.createContext)(null),g=P.Provider;function A(){let e=(0,c.useContext)(P);if(null===e)throw Error("Store cannot be null, please add a context provider");return e}(0,i.cf)(R,e=>{N.env.NEXT_PUBLIC_DEBUG_LOG&&console.log("snapshot",e)})},4332:function(){}},function(e){e.O(0,[228,895,492,147,331,894,971,23,744],function(){return e(e.s=31)}),_N_E=e.O()}]);