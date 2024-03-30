<template>
        <div class="row" style="display:flex; justify-content: center; margin:0 60px; margin-top: 20px;">
        <!--Booking 1-->
            <table class="table rounded-3 table-bordered" style="border-style:solid; border-color: #0D6FE5; border-width: thin;">
                <thead style="background-color: #0DB4F3;">
                <tr>
                    <th class="p-3 d-flex justify-content-start" style="padding-right: 20px; padding-left: 20px;">
                        <i style="border-radius:100%; border-color: grey; color: white; background-color: grey;" class="fa fa-user fa-2x fa-border"></i>
                            <p class="h5 my-auto ms-3">Passenger 1
                                <section class="h5 fw-normal my-auto ms-2 ">- Adult</section>
                            </p>
                    </th>
                </tr>
                </thead>
                <tbody class="text-start" style="background-color: white;">
                <tr>
                    <td style="padding-top:20px;">
                        <!-- Add flight duration -->
                        <h5>Personal details</h5>
                        <div class="row">
                            <div class="col-2">
                                <select class="form-select " aria-label="Default select example" required>
                                    <option disabled selected value="">Title</option>
                                    <option value="1">Mr.</option>
                                    <option value="2">Mrs.</option>
                                    <option value="3">Ms.</option>
                                    <option value="4">Mdm.</option>
                                </select>
                            </div>
                            <div class="col-4 ms-5">
                                <input class="text p-1 ps-2" name="firstName" size="60" type="text" placeholder="First/Given name (as in passport)" required>
                            </div>
                            <div class="col-1 ms-2">
                                <input class="text p-1 ps-2" name="lastName" size="60" type="text" placeholder="Last/Family name (as in passport)" required>
                            </div>
                        </div>
                        <div class="row">
                            <div class="form-check ms-3 mt-3"> 
                                <input class="form-check-input" type="checkbox" value="" id="flexCheckDefault"> 
                                <label class="form-check-label" for="flexCheckDefault"> 
                                    I do not have a first/given name in my passport
                                    </label> 
                                </div> 
                            </div>
                        <div class="row">
                            <div class="form-check ms-3 mt-3"> 
                                <input class="form-check-input" type="checkbox" value="underAge" id="flexCheckDefault"> 
                                <label class="form-check-label" for="flexCheckDefault"> 
                                    I am under 18 years old
                                </label> 
                            </div> 
                        </div>
                        <h5 class="mt-4">Contact details</h5>
                        <div class="col-5 mb-3">
                            <label for="userEmail" class="form-label">Email address</label>
                            <input type="email" class="form-control" id="userEmail1" required>
                        </div>
                    </td>
                </tr>
                </tbody>
            </table>
    </div>
    
    <div class="d-flex justify-content-end">
        <input class="btn btn-primary px-4 mb-3 mt-1 me-5" type="submit" value="Next: Seat Selection">
    </div>
</template>