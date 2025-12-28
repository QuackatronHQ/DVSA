import React from 'react';
import { connect } from 'react-redux';
import { Link } from 'react-router-dom';
import { Button, Container, Header, Form, Dimmer, Loader, Image, Segment  } from 'semantic-ui-react';
import * as API from '../utils/apiCaller';
import {Redirect} from 'react-router-dom';

export class ShippingPage extends React.Component {
    constructor(props){
        super(props);
        this.state = {
            isLoading: false,
            toBilling: false,
            submitted: false,
            shippingInfo: {
                name: '',
                address: '',
                email: '',
                phone: ''
            }
        }
        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    componentDidMount() {
        let shippingInfo = {...this.state.shippingInfo};
        try {
            var userData = JSON.parse(localStorage.getItem("AccountData"));
            if (typeof userData["email"] != "unidentified" ) {
                shippingInfo["email"] = userData["email"]
            }
             if (typeof userData["address"] != "unidentified" ) {
                    shippingInfo["address"] = userData["address"]
            }
             if (typeof userData["phone"] != "unidentified" ) {
                    shippingInfo["phone"] = userData["phone"]
            }
             if (typeof userData["fullname"] != "unidentified" ) {
                   shippingInfo["name"] = userData["fullname"]
            }
        }
        catch (err) {
            console.log(err);
            // nothing
        }
        //console.log(this.state.shippingInfo);
    }
            return <Redirect to='/billing' />
        }
        return(
            <Container className='page-top-margin'>
                <div>
                <Header as='h2'>Enter Shipping Details</Header>
                    {this.state.isLoading && <img src="/images/loader.gif" /> }
                    <Form>
                        <Form.Field>
                        <label>Name</label>
                        <input placeholder='Name' value={this.state.shippingInfo.name} onChange={this.handleChange('name')}/>
                        </Form.Field>
                        <Form.Field>
                        <label>Address</label>
                        <input placeholder='Address' value={this.state.shippingInfo.address} onChange={this.handleChange('address')}/>
                        </Form.Field>
                        <Form.Field>
                        <label>Email  (you will receive a receipt with a link 😀 ) </label>
                        <input disabled placeholder='Email' value={this.state.shippingInfo.email}/>
                        </Form.Field>
                        <Form.Field>
                        <label>Phone</label>
                        <input placeholder='Phone' value={this.state.shippingInfo.phone} onChange={this.handleChange('phone')}/>
                        </Form.Field>
                        <Button type='submit' onClick={this.handleSubmit} disabled={this.state.submitted}>Submit</Button>
                    </Form>
                </div>
            </Container>
        );
    }
}

const mapStateToProps = (state) => ({
    cart: state.shoppingCart
});

export default connect(mapStateToProps)(ShippingPage);