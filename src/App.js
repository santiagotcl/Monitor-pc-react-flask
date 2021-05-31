import React from 'react';
import './App.css';
import Box from './Box';

class App extends React.Component{

  //function App() {
  
  //  this.state = {
  //    options: [{name: 'Srigar', id: 1},{name: 'Sam', id: 2}]
  //};
  
  



    constructor(props) {
    super(props);
    this.state = {
      nucs: []
    };
    /*fetch('http://127.0.0.1:5000/whoisworking',
    { method: 'GET',
    mode: 'no-cors', // <---
    cache: 'default'
 })
    .then((resp) => resp.json())
    .then(function(data) {
      let requesturl = data.results;
      return requesturl.map(item =>
        this.state.nucs.append(item)
      )
    })
    .catch(function(error) {
      console.log(error);
    });*/


 
  }



  componentWillMount() {
    fetch('http://127.0.0.1:5000/whoisworking',
    { method: 'GET',
    mode: 'cors', // <---
    cache: 'default',
    dataType: 'json',
    headers: {
        'Accept': 'application/json'
    }  
 })
    .then(response => response.json())
    .then(data => this.setState({nucs : data},
      () => console.log(this.state.nucs)))

}
  
  //var selectedList = null;
  //var selectedItem = null;
  //var removedItem = null;
  
  /*  onSelect(selectedList, selectedItem){
      this.setState({
          list: selectedList}, () => {
            console.log(this.state.list)
          });
      
      console.log(selectedList)
      console.log(selectedItem)
    };
  
    onRemove(selectedList, removedItem){
      this.setState({
        list: selectedList}, () => {
          console.log(this.state.list)
        });
      console.log(removedItem);
      console.log(selectedList);
    }
  
  print(event){
    console.log(this.state.list)
  }*/
  
    render(){
    return (
      <div className="App">
        <header className="App-header">
        {
          this.state.nucs.map(item => <Box names={item}/>)
        }
        </header>
      </div>
    );
  }
  }
  //}
  
  export default App;
