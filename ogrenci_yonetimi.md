# Genel Tanımlama
Bu proje **Flask** kullanarak yapacağınız basit bir web uygulamasıdır.
Sizden şu an için template tarafı ile uğraşmanızı istemiyorum.
Bu uygulamada şu an için bütün işlerimiz Json istekleri şeklinde çalışacak.

# Veritabanı
Veritabanı konusunda şu ana kadar kullandığımız ilkel **Json** dosyası yöntemini kullanabilirsiniz.
Ama uğraşmak isterseniz [**Sqlite**](https://flask.palletsprojects.com/en/2.2.x/tutorial/database/) da kullanabilirsiniz.
İsteyen de NoSQL bir veri tabanı kullanabilir. Burada **MongoDB** güzel bir seçenektir.

# Programın özellikleri

## Veriler
* Ders
    * ID
    * gün/saat
    * sınıf odası
    * öğretmen
* Öğrenci
    * ID
    * ad
    * soyad
    * yas
    * sınıflar (sınıf objelerine bağlı ya da idlerine bağlı olacak)
* Not
    * Öğrenci (Tek bir öğrenci ögesine bağlı)
    * Sınıf (Tek bir sınıf ögesine bağlı)
    * değer (Notun int değeri)
* Loglar
    * İşlem yapılan model
    * İşlem tipi
    * İşlem tarihi ve saati
    * Açıklama

## Programın yapabilmesi gereken şeyler:
* Öğrenci oluşturma - OK
* Öğrenci listeleme - OK
* Öğrencinin detaylarını görme - OK
* Öğrenci çıkartma
* Ders oluşturma - OK
* Ders listeleme - OK
* Ders silme
* Derse kayıtlı bütün öğrencileri listeleme - OK
* Öğrenciye ders ekleme - OK
* Öğrenciye derse göre not ekleme - OK
* Öğrencinin o ders içerisindeki notlarını listeleme - OK
* Öğrencinin bütün notlarını listeleme - OK
* Öğrencinin not ortalamasını hesaplama - OK

## Dikkat edilmesi gerekenler
* Her bir işlem ardından veri tabanına kayıt ve gerekiyorsa log yapılması
* Dosyaların düzgün organize edilmesi
* gitignore dosyasına dikkat edilmesi
* url düzeninin düzgün bir hiyerarşide kurulması
