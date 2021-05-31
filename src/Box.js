import './Box.css';
import React from 'react';



class Box extends React.Component{ 
    
    render(){
    return (
        <div className="Conteiner" className={this.props.names.Color}>
        <div ClassName='title'>{this.props.names.Linea}</div>
        <div className="pc">
            <div className="firstline">
            <div>{this.props.names.Name}</div>
            </div>

            <div>{this.props.names.IP}</div>
        </div>
        </div>
    );
  }
  }
  //}
  
  export default Box;