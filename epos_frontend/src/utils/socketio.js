

import io from 'socket.io-client';
import { websocket_port } from "../../../../../sites/common_site_config.json"

let host = window.location.hostname;
let protocol = window.location.protocol;
let port ="";

if (protocol=="http:"){
    port = ":" +  websocket_port;
} 
 
 
let socket = io(protocol + "//" + host + port, { path: '/socketserver/socket.io' });

export default socket;

