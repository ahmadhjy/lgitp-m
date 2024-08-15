import React, { useState } from 'react';
import './ImageCatalog.css';

const ImageCatalog = ({ imageLinks }) => {
  const [showModal, setShowModal] = useState(false);
  const [currentIndex, setCurrentIndex] = useState(0);

  const openModal = (index) => {
    setCurrentIndex(index);
    setShowModal(true);
  };

  const closeModal = () => setShowModal(false);

  const nextImage = () => setCurrentIndex((prevIndex) => (prevIndex + 1) % imageLinks.length);

  const prevImage = () => setCurrentIndex((prevIndex) => (prevIndex - 1 + imageLinks.length) % imageLinks.length);

  return (
    <div>
      <div className="image-catalog">
        {imageLinks.slice(0, 3).map((link, index) => (
          <img key={index} src={link} alt={`Image ${index}`} onClick={() => openModal(index)} className="catalog-image" />
        ))}
        {imageLinks.length > 3 && (
          <div className="more-images" onClick={() => openModal(3)}>
            +{imageLinks.length - 3}
          </div>
        )}
      </div>
      {showModal && (
        <div className="modal">
          <span className="close" onClick={closeModal}>&times;</span>
          <img src={imageLinks[currentIndex]} alt={`Image ${currentIndex}`} className="modal-image" />
          <button className="prev" onClick={prevImage}>&#10094;</button>
          <button className="next" onClick={nextImage}>&#10095;</button>
        </div>
      )}
    </div>
  );
};

export default ImageCatalog;
