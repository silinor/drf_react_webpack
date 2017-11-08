import React from 'react';
import ReactDOM from 'react-dom';
import { request } from "./utils"

class RootComponent extends React.Component {
  constructor(props) {
    super(props);
    this.state = {users: []};
  }

  componentDidMount() {
    this.getUsers();
  }

  getUsers() {
    let self = this;
    request('/api/user/').then(function (users) {
       self.setState({users: users})
    });
  }

  render() {
    return (
        <div className="row">
          <div className="col-xs-12">
            <UsersMoneySendForm users={this.state.users}/>
          </div>
        </div>
    );
  }
}

class UsersMoneySendForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = {btnDisable: false, error: false, message: false};
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleChange(event) {
    const target = event.target;
    const value = target.value;
    const name = target.name;

    this.setState({
      [name]: value
    });
  }

  handleSubmit(event) {
    let self = this;
    this.setState({btnDisable: true});
    let form = new FormData(document.getElementById('usersMoneySendForm'));
    request('/api/user/money_transfer/', {method: 'POST', body: form}).then(function (resp) {
      self.setState({btnDisable: false});
      if (resp['error']) {
        self.setState({error: resp['error']});
      } else {
        self.setState({error: false});
      }
      if (resp['message']) {
        self.setState({message: resp['message']});
      } else {
        self.setState({message: false});
      }
    });
    event.preventDefault();
  }

  render() {
    let options = []
    this.props.users.forEach(user => options.push(<UserSelectOption user={user} key={user.id} />))
    return (
        <form onSubmit={this.handleSubmit} id="usersMoneySendForm">
          { this.state.error &&
            <div className="alert alert-danger">
              {this.state.error}
            </div>
          }
          { this.state.message &&
            <div className="alert alert-success">
              {this.state.message}
            </div>
          }
          <div className="form-group">
            <label>Select user:</label>
            <select value={this.state.usersSelect} onChange={this.handleChange} className="form-control" name="usersSelect">
              {options}
            </select>
          </div>
          <div className="form-group">
            <label>INN:</label>
            <input type="text" className="form-control" value={this.state.inn} name="inn" required />
            <small className="form-text text-muted">
              INN list separated with comma ','
            </small>
          </div>
          <div className="form-group">
            <label>Amount:</label>
            <input type="number" className="form-control" value={this.state.amount} name="amount" required  />
          </div>
          <div className="form-group">
            <input type="submit" value="Submit" className="btn btn-primary" disabled={this.state.btnDisable} />
          </div>
        </form>
    );
  }
}

class UserSelectOption extends React.Component {
  render() {
    return (
        <option value={this.props.user.id}>{this.props.user.username}</option>
    );
  }
}


ReactDOM.render(
  <RootComponent />,
  document.getElementById('container')
);