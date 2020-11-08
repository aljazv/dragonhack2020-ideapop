import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import { API_URL } from './env';
import { saveAs } from "file-saver";

@Injectable()
export class AppService {

  constructor(private http: HttpClient) {
  }

  

  sendCoordinates(coordinates) {
    this.http.post(`${API_URL}/coordinates`, coordinates, {
      responseType: "blob",
    }).subscribe(
      data => {
        saveAs(data, "nesejne.png");
      },
    );
  }
}
