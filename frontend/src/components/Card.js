import { MainUrl } from '../services/api';
import "./Card.css";
import { FaMapMarkerAlt, FaClock, FaDollarSign, FaTag } from 'react-icons/fa';

const Card = ({ item, onClick }) => (
  <div className="card" onClick={onClick}>
    <div className="card-image-wrapper">
      <img src={`${MainUrl}/${item.image}`} alt={item.title} />
    </div>
    <div className="card-content">
      <h2>{item.title}</h2>
      <div className="card-details">
        <p className="card-location"><FaMapMarkerAlt className='card-icon'/> {item.location.name}</p>
        <p className="card-to"><FaClock className='card-icon'/> Available till {item.available_to}</p>
        {/* <p className="card-category"><FaTag className='card-icon'/> {item.categories.map(cat => cat.name).join(', ')}</p> */}
      </div>
      <div className="card-price"><FaDollarSign /> {item.offers[0].price} <span>per {item.unit}</span></div>
    </div>
  </div>
);

export default Card;
