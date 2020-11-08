import { Component, OnInit } from '@angular/core';
import { icon, latLng, latLngBounds, MapOptions, Marker, rectangle, tileLayer } from 'leaflet';
import { AppService } from "../app.service";



@Component({
  selector: 'app-map',
  templateUrl: './map.component.html',
  styleUrls: ['./map.component.scss']
})
export class MapComponent implements OnInit {

  map: any;
  mapOptions: MapOptions;
  value: number = 1;

  constructor(private _service: AppService) { }

  ngOnInit() {
    this.initializeMapOptions();
  }

  onMapReady(map: any) {
    this.map = map;
    this.addSampleMarker(46.0569, 14.5058);
  }

  onChange(event) {
    this.value = event.value;

  }

  onMapClick(event) {
    //console.log(this.value);
    
    const moveLat = 0.02 * this.value * this.value;
    const moveLng = 0.02*1.5 * this.value * this.value;

    const coordinateLat = event.latlng.lat;
    const coordinateLng = event.latlng.lng;
    const center = latLng(coordinateLat, coordinateLng);

    const corner1 = latLng(coordinateLat - moveLat, coordinateLng - moveLng);
    const corner2 = latLng(coordinateLat + moveLat, coordinateLng + moveLng);
    const bounds = latLngBounds(corner1, corner2);
    rectangle(bounds, {color: '#800000'}).addTo(this.map);
    //this.map.fitBounds(bounds);

    this.addSampleMarker(coordinateLat,coordinateLng);

    const data = {
      leftBottomLat: coordinateLat - moveLat,
      leftBottomLng: coordinateLng - moveLng,
      rightTopLat: coordinateLat + moveLat,
      rightTopLng: coordinateLng + moveLng
    }
    this._service.sendCoordinates(data);
  }

  private initializeMapOptions() {
    this.mapOptions = {
      center: latLng(46.0569, 14.5058),
      zoom: 12,
      layers: [
        tileLayer(
          'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
          {
            maxZoom: 18,
            attribution: 'Map data © OpenStreetMap contributors'
          })
      ],
    };
  }

  private addSampleMarker(coordinateX, coordinateY) {
    const marker = new Marker([coordinateX, coordinateY])
      .setIcon(
        icon({
          iconSize: [25, 41],
          iconAnchor: [13, 41],
          iconUrl: 'assets/marker-icon.png'
        }));
    marker.addTo(this.map);
  }
}
