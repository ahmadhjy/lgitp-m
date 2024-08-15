import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";
import Card from "./Card";
import "./Favorites.css";

const Favorites = () => {
    const [favorites, setFavorites] = useState({ activities: [], tours: [], packages: [] });
    const navigate = useNavigate();

    useEffect(() => {
        const fetchFavorites = async () => {
            try {
                const response = await api.get('/api/all-favorites/');
                setFavorites(response.data);
            } catch (error) {
                console.error("Failed to fetch favorites", error);
            }
        };

        fetchFavorites();
    }, []);

    const handleCardClick = (id, type) => {
        navigate(`/${type}-details/${id}`);
    };

    return (
        <div className="favorites-container">
            <h1>My Favorites</h1>
            <div className="favorites-list">
                {favorites.activities.map((fav) => (
                    <Card key={fav.activity.id} item={fav.activity} onClick={() => handleCardClick(fav.activity.id, 'activity')} />
                ))}
                {favorites.tours.map((fav) => (
                    <Card key={fav.tour.id} item={fav.tour} onClick={() => handleCardClick(fav.tour.id, 'tour')} />
                ))}
                {favorites.packages.map((fav) => (
                    <Card key={fav.package.id} item={fav.package} onClick={() => handleCardClick(fav.package.id, 'package')} />
                ))}
            </div>
        </div>
    );
};

export default Favorites;
